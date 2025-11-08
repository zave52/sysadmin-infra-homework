"""Molecule tests for web role"""

import pytest


@pytest.fixture
def nginx_container(host):
    """Skip test if not running on nginx container"""
    if host.backend.get_hostname() != "nginx-molecule":
        pytest.skip("Test only runs on nginx container")


@pytest.fixture
def php_container(host):
    """Skip test if not running on php-fpm container"""
    if host.backend.get_hostname() != "php-fpm-molecule":
        pytest.skip("Test only runs on php-fpm container")


def test_container_accessible(host):
    """Verify connection to container"""
    assert host.backend.get_hostname() in ["nginx-molecule", "php-fpm-molecule"]


class TestNginxContainer:
    """Tests specific to nginx container"""

    def test_php_files_deployed(self, host, nginx_container):
        """Verify PHP files exist with correct permissions"""
        for filename in ["index.php", "healthz.php"]:
            file = host.file(f"/var/www/html/{filename}")
            assert file.exists
            assert file.is_file

    def test_logrotate_configured(self, host, nginx_container):
        """Verify logrotate is installed and configured"""
        assert host.exists("logrotate")

        config = host.file("/etc/logrotate.d/nginx")
        assert config.exists
        assert config.mode == 0o644
        assert config.contains("daily")
        assert config.contains("rotate 14")

    def test_cron_service_active(self, host, nginx_container):
        """Verify cron service is running"""
        cron_check = host.run("pidof cron || pgrep -x cron")
        assert cron_check.rc == 0

    def test_nginx_configuration_valid(self, host, nginx_container):
        """Verify nginx configuration passes validation"""
        result = host.run("nginx -t")
        assert result.rc == 0

    def test_nginx_process_running(self, host, nginx_container):
        """Verify nginx master and worker processes are running"""
        result = host.run("pgrep -f 'nginx: master process'")
        assert result.rc == 0

    def test_health_endpoint_response(self, host, nginx_container):
        """Verify health endpoint returns correct JSON"""
        result = host.run("curl -sf http://localhost/healthz")
        assert result.rc == 0
        assert '"status":"ok"' in result.stdout
        assert '"service":"nginx"' in result.stdout
        assert '"env":"test"' in result.stdout

    def test_main_page_accessible(self, host, nginx_container):
        """Verify main page is accessible"""
        result = host.run("curl -sf http://localhost/")
        assert result.rc == 0
        assert "PHP Version" in result.stdout


class TestPhpFpmContainer:
    """Tests specific to php-fpm container"""

    def test_php_fpm_process_running(self, host, php_container):
        """Verify PHP-FPM master and worker processes are running"""
        result = host.run("pgrep -f 'php-fpm: master process'")
        assert result.rc == 0

    def test_php_fpm_listening(self, host, php_container):
        """Verify PHP-FPM is listening on port 9000"""
        result = host.run("netstat -tln | grep ':9000'")
        assert result.rc == 0

    def test_php_files_exist(self, host, php_container):
        """Verify PHP files are accessible in shared volume"""
        for filename in ["index.php", "healthz.php"]:
            file = host.file(f"/var/www/html/{filename}")
            assert file.exists
            assert file.is_file

    def test_app_env_variable_set(self, host, php_container):
        """Verify APP_ENV environment variable is set"""
        result = host.run("printenv APP_ENV")
        assert result.rc == 0
        assert result.stdout.strip() == "test"

    def test_php_version(self, host, php_container):
        """Verify PHP version is 8.4"""
        result = host.run("php -v")
        assert result.rc == 0
        assert "PHP 8.4" in result.stdout

    def test_php_fpm_config_valid(self, host, php_container):
        """Verify PHP-FPM configuration is valid"""
        result = host.run("php-fpm -t")
        assert result.rc == 0
