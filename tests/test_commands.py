from unittest import TestCase
from unittest.mock import patch, Mock, mock_open
from click.testing import CliRunner
from commands import file_upload, file_download


@patch("commands.requests")
@patch("commands.os.path.exists")
class TestFileUpload(TestCase):
    runner = CliRunner()

    def test__file_upload__local_file_exist_and_response_success(
        self, patch_exists, patch_requests
    ):

        patch_open_file = patch("commands.open", mock_open())
        mock_post_res = Mock()
        mock_post_res.status_code = 200
        patch_exists.return_value = True
        patch_requests.post.return_value = mock_post_res

        with patch_open_file, patch_exists, patch_requests:
            result = self.runner.invoke(
                file_upload,
                ["--remote-path", "/remote_file.txt", "--local-path", "local_file.txt"],
            )

        self.assertEqual(
            result.output,
            "uploading ..\nfile local_file.txt successfully upload to /remote_file.txt\n",
        )
        patch_requests.post.assert_called_once()
        patch_exists.assert_called_once()

    def test__file_upload__local_file_exist_and_response_error(
        self, patch_exists, patch_requests
    ):
        patch_open_file = patch("commands.open", mock_open())
        mock_post_res = Mock()
        mock_post_res.status_code = 400
        mock_post_res.text = "fake error"
        patch_exists.return_value = True
        patch_requests.post.return_value = mock_post_res

        with patch_open_file, patch_exists, patch_requests:
            result = self.runner.invoke(
                file_upload,
                ["--remote-path", "/remote_file.txt", "--local-path", "local_file.txt"],
            )

        self.assertEqual(
            result.output,
            "uploading ..\nsomething went wrong and the file local_file.txt could't be upload\nreason: fake error\n",
        )
        patch_requests.post.assert_called_once()
        patch_exists.assert_called_once()

    def test__file_upload__local_not_file_exist(self, patch_exists, patch_requests):

        patch_exists.return_value = False

        runner = CliRunner()

        with patch_exists:
            result = runner.invoke(
                file_upload,
                ["--remote-path", "/remote_file.txt", "--local-path", "local_file.txt"],
            )

        self.assertEqual(
            result.output, "File with path local_file.txt doesn't exist\n",
        )
        patch_requests.post.assert_not_called()
        patch_exists.assert_called()


@patch("commands.requests")
@patch("commands.os.path.exists")
class TestFileDownload(TestCase):

    runner = CliRunner()

    def test__file_download__response_success(self, patch_exists, patch_requests):

        patch_open_file = patch("commands.open", mock_open())
        patch_exists.return_value = False
        mock_post_res = Mock()
        mock_post_res.status_code = 200
        patch_requests.post.return_value = mock_post_res

        with patch_open_file, patch_exists, patch_requests:
            result = self.runner.invoke(
                file_download,
                ["--remote-path", "/file.txt", "--local-path", "file.txt"],
            )

        self.assertEqual(
            result.output, "file /file.txt successfully downloaded to file.txt\n"
        )
        patch_exists.assert_called_once()
        patch_requests.post.assert_called_once()

    def test__file_download__overwrite_local_path_response_success(
        self, patch_exists, patch_requests
    ):

        patch_open_file = patch("commands.open", mock_open())
        patch_click_getchar = patch("commands.click.getchar")
        patch_click_getchar.return_value = "y"
        patch_exists.return_value = True
        mock_post_res = Mock()
        mock_post_res.status_code = 200
        patch_requests.post.return_value = mock_post_res

        with patch_open_file, patch_exists, patch_requests, patch_click_getchar:
            result = self.runner.invoke(
                file_download,
                ["--remote-path", "/file.txt", "--local-path", "file.txt"],
            )

        self.assertEqual(
            result.output,
            "File with path file.txt exist, are you sure you want to overwrite?[y/n]file /file.txt successfully downloaded to file.txt\n",
        )

    def test__file_download__do_not_overwrite_local_path(
        self, patch_exists, patch_requests
    ):

        patch_open_file = patch("commands.open", mock_open())
        patch_click_getchar = patch("commands.click.getchar")
        patch_click_getchar.return_value = "n"
        patch_exists.return_value = True
        mock_post_res = Mock()
        mock_post_res.status_code = 200
        patch_requests.post.return_value = mock_post_res

        with patch_open_file, patch_exists, patch_requests, patch_click_getchar:
            result = self.runner.invoke(
                file_download,
                ["--remote-path", "/file.txt", "--local-path", "file.txt"],
            )

        self.assertEqual(
            result.output,
            "File with path file.txt exist, are you sure you want to overwrite?[y/n]file /file.txt successfully downloaded to file.txt\n",
        )
