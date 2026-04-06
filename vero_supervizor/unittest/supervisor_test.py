import sys
from pathlib import Path
_repo_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_repo_root))

import json
import queue
import threading
import unittest
from unittest.mock import MagicMock, patch

from vero_supervizor.supervisor_client import SupervisorClient, SupervisorDataFactory
from vero_supervizor.supervisor_enum import TaskType, ReportCondition
from vero_supervizor.supervizor_host import SupervisorHost


class TestSupervisorDataFactory(unittest.TestCase):
    def setUp(self):
        SupervisorDataFactory._factory_obj = None

    def test_singleton_and_register_payload(self):
        factory = SupervisorDataFactory()
        same_factory = SupervisorDataFactory()

        payload = factory.register(
            "proc-1",
            {"k": "v"},
            response=True,
            regular=False,
            update=True,
            finish=True,
        )

        self.assertIs(factory, same_factory)
        self.assertEqual(payload["task"], TaskType.REGISTER)
        self.assertEqual(payload["proc_name"], "proc-1")
        self.assertEqual(payload["data"], {"k": "v"})
        self.assertIsInstance(payload["report_condition"], ReportCondition)
        self.assertTrue(payload["report_condition"].RESPONSE)
        self.assertFalse(payload["report_condition"].REGULAR)
        self.assertTrue(payload["report_condition"].UPDATE)
        self.assertTrue(payload["report_condition"].FINISH)
        self.assertIn("proc-1", factory.proc_lst)

    @patch("vero_supervizor.supervisor_client.logger.warning")
    def test_register_duplicate_process_logs_warning(self, mock_warning):
        factory = SupervisorDataFactory()
        factory.register("proc-dup", {"x": 1})
        factory.register("proc-dup", {"x": 2})

        self.assertEqual(factory.proc_lst.count("proc-dup"), 1)
        mock_warning.assert_called_once()

    def test_update_registered_process(self):
        factory = SupervisorDataFactory()
        factory.register("proc-updated", {"init": True})

        payload = factory.update("proc-updated", {"step": 2})

        self.assertEqual(
            payload,
            {
                "task": TaskType.UPDATE,
                "proc_name": "proc-updated",
                "data": {"step": 2},
            },
        )

    @patch("vero_supervizor.supervisor_client.logger.warning")
    def test_update_unregistered_process_falls_back_to_register(self, mock_warning):
        factory = SupervisorDataFactory()

        payload = factory.update("new-proc", {"step": 1})

        self.assertEqual(payload["task"], TaskType.REGISTER)
        self.assertEqual(payload["proc_name"], "new-proc")
        self.assertEqual(payload["data"], {"step": 1})
        self.assertIn("new-proc", factory.proc_lst)
        mock_warning.assert_called_once()

    def test_finish_registered_process(self):
        factory = SupervisorDataFactory()
        factory.register("proc-finish", {"init": True})

        payload = factory.finish("proc-finish")

        self.assertEqual(
            payload,
            {
                "task": TaskType.FINISH,
                "proc_name": "proc-finish",
            },
        )

    @patch("vero_supervizor.supervisor_client.logger.warning")
    def test_finish_unregistered_process_returns_none(self, mock_warning):
        factory = SupervisorDataFactory()

        payload = factory.finish("missing-proc")

        self.assertIsNone(payload)
        mock_warning.assert_called_once()


class TestSupervisorClient(unittest.TestCase):
    @patch("vero_supervizor.supervisor_client.threading.Thread")
    def test_init_creates_worker_thread(self, mock_thread):
        fake_thread = MagicMock()
        mock_thread.return_value = fake_thread

        client = SupervisorClient(host="1.2.3.4", port=7777, max_queue_size=7)

        self.assertEqual(client.host, "1.2.3.4")
        self.assertEqual(client.port, 7777)
        self.assertEqual(client.queue.maxsize, 7)
        mock_thread.assert_called_once_with(target=client._worker, daemon=True)
        fake_thread.start.assert_called_once()

    @patch("vero_supervizor.supervisor_client.time.sleep")
    @patch("vero_supervizor.supervisor_client.socket.socket")
    def test_connect_retries_until_success(self, mock_socket_cls, _mock_sleep):
        first_sock = MagicMock()
        second_sock = MagicMock()
        first_sock.connect.side_effect = OSError("connect failed")
        second_sock.connect.return_value = None
        mock_socket_cls.side_effect = [first_sock, second_sock]

        client = SupervisorClient.__new__(SupervisorClient)
        client.host = "127.0.0.1"
        client.port = 5000
        client.running = True
        client.sock = None

        client._connect()

        self.assertIs(client.sock, second_sock)
        self.assertEqual(mock_socket_cls.call_count, 2)

    def test_worker_sends_framed_json(self):
        client = SupervisorClient.__new__(SupervisorClient)
        client.running = True
        client.sock = MagicMock()
        client._connect = MagicMock()
        client.queue = MagicMock()
        payload = {"task": "update", "value": 1}
        client.queue.get.side_effect = [payload, queue.Empty()]

        def stop_after_send(data):
            client.running = False

        client.sock.sendall.side_effect = stop_after_send

        client._worker()

        expected_msg = json.dumps(payload).encode("utf-8")
        expected_packet = len(expected_msg).to_bytes(4, "big") + expected_msg
        client.sock.sendall.assert_called_once_with(expected_packet)
        client._connect.assert_called_once()

    def test_worker_reconnects_after_send_error(self):
        client = SupervisorClient.__new__(SupervisorClient)
        client.running = True
        client.sock = MagicMock()
        client.queue = MagicMock()
        client.queue.get.return_value = {"task": "update"}
        client.sock.sendall.side_effect = RuntimeError("send failed")
        connect_calls = {"count": 0}

        def connect_hook():
            connect_calls["count"] += 1
            if connect_calls["count"] >= 2:
                client.running = False

        client._connect = MagicMock(side_effect=connect_hook)

        client._worker()

        self.assertGreaterEqual(client._connect.call_count, 2)

    @patch("vero_supervizor.supervisor_client.logger.warning")
    def test_send_drops_data_when_queue_full(self, mock_warning):
        client = SupervisorClient.__new__(SupervisorClient)
        client.queue = MagicMock()
        client.queue.put_nowait.side_effect = queue.Full

        client.send({"task": "x"})

        mock_warning.assert_called_once()

    def test_close_sets_running_false_and_closes_socket(self):
        client = SupervisorClient.__new__(SupervisorClient)
        client.running = True
        client.sock = MagicMock()

        client.close()

        self.assertFalse(client.running)
        client.sock.close.assert_called_once()


class TestSupervisorHost(unittest.TestCase):
    @patch("vero_supervizor.supervizor_host.threading.Thread")
    @patch("vero_chat_agent.MailBox")
    def test_init_email_creates_mailbox_and_listener_thread(self, mock_mailbox, mock_thread):
        fake_thread = MagicMock()
        mock_thread.return_value = fake_thread
        actions = MagicMock()
        message_cfg = {
            "type": "email",
            "sender": "sender@test.com",
            "receivers": ["a@test.com"],
            "mail_params": {"mail_host": "x", "mail_user": "u", "mail_pass": "p"},
        }

        host = SupervisorHost(port=6000, actions=actions, message_cfg=message_cfg)

        mock_mailbox.assert_called_once_with(message_cfg["mail_params"])
        mock_thread.assert_called_once_with(target=host.start_listen, daemon=True)
        fake_thread.start.assert_called_once()

    @patch("vero_supervizor.supervizor_host.threading.Thread")
    @patch("vero_chat_agent.WeChat")
    def test_init_wechat_creates_wechat_and_listener_thread(self, mock_wechat, mock_thread):
        fake_thread = MagicMock()
        mock_thread.return_value = fake_thread
        actions = MagicMock()
        message_cfg = {"type": "wechat", "receivers": ["wxid_1"]}

        host = SupervisorHost(port=6001, actions=actions, message_cfg=message_cfg)

        mock_wechat.assert_called_once_with()
        mock_thread.assert_called_once_with(target=host.start_listen, daemon=True)
        fake_thread.start.assert_called_once()

    @patch("vero_supervizor.supervizor_host.threading.Thread")
    @patch("vero_supervizor.supervizor_host.socket.socket")
    def test_start_listen_accepts_connection_and_spawns_handler_thread(self, mock_socket_cls, mock_thread):
        host = SupervisorHost.__new__(SupervisorHost)
        host.host = "0.0.0.0"
        host.port = 5000
        host.running = True

        fake_server_socket = MagicMock()
        fake_conn = MagicMock()
        fake_addr = ("127.0.0.1", 8000)
        fake_server_socket.__enter__.return_value = fake_server_socket

        def accept_once():
            host.running = False
            return fake_conn, fake_addr

        fake_server_socket.accept.side_effect = accept_once
        mock_socket_cls.return_value = fake_server_socket
        fake_thread = MagicMock()
        mock_thread.return_value = fake_thread

        host.start_listen()

        fake_server_socket.bind.assert_called_once_with((host.host, host.port))
        fake_server_socket.listen.assert_called_once()
        mock_thread.assert_called_once_with(
            target=host._handle_client,
            args=(fake_conn, fake_addr),
            daemon=True,
        )
        fake_thread.start.assert_called_once()

    def test_handle_client_parses_framed_messages(self):
        host = SupervisorHost.__new__(SupervisorHost)
        host.running = True
        host.handle_msg = MagicMock()
        conn = MagicMock()
        addr = ("127.0.0.1", 9000)
        payload = {"task": "update", "proc_name": "p1", "data": {"x": 1}}
        raw = json.dumps(payload).encode("utf-8")
        packet = len(raw).to_bytes(4, "big") + raw
        conn.recv.side_effect = [packet[:5], packet[5:], b""]

        host._handle_client(conn, addr)

        host.handle_msg.assert_called_once_with(payload)
        conn.close.assert_called_once()

    def test_handle_client_logs_decode_error_but_keeps_running(self):
        host = SupervisorHost.__new__(SupervisorHost)
        host.running = True
        host.handle_msg = MagicMock()
        conn = MagicMock()
        addr = ("127.0.0.1", 9001)
        bad = b"not_json"
        packet = len(bad).to_bytes(4, "big") + bad
        conn.recv.side_effect = [packet, b""]

        with patch("vero_supervizor.supervizor_host.logger.error") as mock_error:
            host._handle_client(conn, addr)

        host.handle_msg.assert_not_called()
        mock_error.assert_called()
        conn.close.assert_called_once()

    @patch("vero_supervizor.supervizor_host.ProcessAgent")
    @patch("vero_supervizor.supervizor_host.ProcessAgentActions")
    def test_handle_msg_register_uses_default_actions_when_missing(self, mock_actions_cls, mock_agent_cls):
        host = SupervisorHost.__new__(SupervisorHost)
        host.processes = {}
        host.actions = MagicMock()
        host.actions.custom_actions = {"update": []}
        host.message_cfg = {"type": "wechat", "receivers": ["u1"]}
        host.processes_lock = threading.Lock()
        host.transceiver_lock = threading.Lock()
        host.message_transceiver = MagicMock()

        default_actions = MagicMock()
        mock_actions_cls.return_value = default_actions
        agent_instance = MagicMock()
        mock_agent_cls.return_value = agent_instance

        msg = {"task": TaskType.REGISTER, "proc_name": "p1"}
        host.handle_msg(msg)

        mock_actions_cls.assert_called_once_with(host.actions.custom_actions)
        mock_agent_cls.assert_called_once()
        self.assertIs(host.processes["p1"], agent_instance)
        host.message_transceiver.send.assert_not_called()

    @patch("vero_supervizor.supervizor_host.logger.error")
    def test_handle_msg_unknown_process(self, mock_error):
        host = SupervisorHost.__new__(SupervisorHost)
        host.processes = {}
        host.processes_lock = threading.Lock()
        host.transceiver_lock = threading.Lock()
        host.message_transceiver = MagicMock()

        host.handle_msg({"task": TaskType.UPDATE, "proc_name": "missing", "data": {}})

        mock_error.assert_called_once()
        host.message_transceiver.send.assert_not_called()

    @patch("vero_supervizor.supervizor_host.logger.error")
    def test_handle_msg_unknown_task(self, mock_error):
        host = SupervisorHost.__new__(SupervisorHost)
        agent = MagicMock()
        host.processes = {"p1": agent}
        host.processes_lock = threading.Lock()
        host.transceiver_lock = threading.Lock()
        host.message_transceiver = MagicMock()

        host.handle_msg({"task": "bad-task", "proc_name": "p1"})

        mock_error.assert_called_once()
        host.message_transceiver.send.assert_not_called()

    def test_handle_msg_update_sends_draft(self):
        host = SupervisorHost.__new__(SupervisorHost)
        agent = MagicMock()
        agent.update.return_value = "draft-content"
        host.processes = {"p1": agent}
        host.processes_lock = threading.Lock()
        host.transceiver_lock = threading.Lock()
        host.message_transceiver = MagicMock()

        host.handle_msg({"task": TaskType.UPDATE, "proc_name": "p1", "data": {"v": 1}})

        agent.update.assert_called_once_with({"v": 1})
        host.message_transceiver.add_draft.assert_called_once_with("draft-content")
        host.message_transceiver.send.assert_called_once()

    def test_handle_msg_finish_without_draft_does_not_send(self):
        host = SupervisorHost.__new__(SupervisorHost)
        agent = MagicMock()
        agent.finish.return_value = None
        host.processes = {"p1": agent}
        host.processes_lock = threading.Lock()
        host.transceiver_lock = threading.Lock()
        host.message_transceiver = MagicMock()

        host.handle_msg({"task": TaskType.FINISH, "proc_name": "p1"})

        agent.finish.assert_called_once_with()
        host.message_transceiver.send.assert_not_called()

    def test_close_marks_host_not_running(self):
        host = SupervisorHost.__new__(SupervisorHost)
        host.running = True

        host.close()

        self.assertFalse(host.running)


if __name__ == "__main__":
    unittest.main()
