# setting up web servers for web_static deployment

# Update the package index
package { 'update':
  ensure => latest,
  command => '/usr/bin/apt-get update',
}

# Upgrade all installed packages
package { 'upgrade':
  ensure => latest,
  command => '/usr/bin/apt-get upgrade -y',
  require => Package['update'],
}

# Install Nginx
package { 'nginx':
  ensure => installed,
}

# Create necessary directories
file { '/data/web_static/':
  ensure => directory,
}

file { '/data/web_static/releases/test/':
  ensure => directory,
}

file { '/data/web_static/shared/':
  ensure => directory,
}

# Create index.html with content
file { '/data/web_static/releases/test/index.html':
  ensure  => present,
  content => 'Holberton School',
}

# Create symbolic link
file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test',
}

# Change ownership of the /data/ directory
exec { 'change_ownership':
  command => '/bin/chown -R ubuntu:ubuntu /data/',
  path    => ['/bin', '/usr/bin'],
}

# Add Nginx configuration for /hbnb_static
file_line { 'nginx_hbnb_static_config':
  path    => '/etc/nginx/sites-available/default',
  line    => '        location /hbnb_static/ {',
  match   => '^(\s+)location / {',
  after   => '^(\s+)location / {',
  require => Package['nginx'],
  notify  => Service['nginx'],
}

file_line { 'nginx_alias_config':
  path    => '/etc/nginx/sites-available/default',
  line    => '                alias /data/web_static/current/;',
  match   => '^(\s+)}',
  after   => '^(\s+)}',
  require => Package['nginx'],
  notify  => Service['nginx'],
}

# Restart Nginx
service { 'nginx':
  ensure => running,
  enable => true,
}

# Notify Nginx restart when configuration changes
Service['nginx'] -> File_line['nginx_hbnb_static_config']
Service['nginx'] -> File_line['nginx_alias_config']

