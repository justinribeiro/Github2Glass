group { 'puppet': 
  ensure => 'present' 
}

class { 'apache': }

# virtual host with alternate options
# you could roll this a lot of different ways
apache::vhost { 'github2glass.vm':
  port => '80',
  docroot => '/vagrant/web',
  options => [
    'FollowSymLinks',
  ],
  override => 'All',
}

# just get some PHP; leave FPM for another day
class php {
  package { "php5":
    ensure => present,
  }
 
  package { "php5-cli":
    ensure => present,
  }
  
  package { 'php5-sqlite': 
	ensure => 'present' 
  }
  
  package { 'php5-curl': 
	ensure => 'present' 
  }
}

class sqlite {
  package { 'sqlite3':
    ensure => 'present',
  }
  
  exec { "create-database":
    path    => ["/bin", "/usr/bin"],
    command => "touch /vagrant/db/github2glass.sqlite"
  }
  
  exec { "database-permissions":
    path    => ["/bin", "/usr/bin"],
    command => "chmod 777 /vagrant/db/github2glass.sqlite",
	require => [Exec["create-database"] ]
  }
}

# We at the very least need the Mosquitto python libs so we can 
# talk to the broker
class mosquitto {
  
  package { "python-software-properties":
    ensure => present,
  }
  
  exec { "recent-mosquitto":
	path    => ["/bin", "/usr/bin"],
	command => "add-apt-repository ppa:mosquitto-dev/mosquitto-ppa && apt-get update",
    require => Package["python-software-properties"],
    creates => "/etc/apt/sources.list.d/mosquitto-dev-mosquitto-ppa-precise.list",
  }  
  
  package { "mosquitto":
    ensure => present,
	require => [Exec["recent-mosquitto"] ]
  }
  
  package { "python-mosquitto":
    ensure => present,
	require => [Exec["recent-mosquitto"] ]
  }
  
  package { "mosquitto-clients":
    ensure => present,
	require => [Exec["recent-mosquitto"] ]
  }  
}

#easy_install or pip...choices, choices
class python {

  package { "python-setuptools":
    ensure => present,
  }
  
  package { "python-pip":
    ensure => present,
  }
  
  exec { "update-google-apis":
    path    => ["/bin", "/usr/bin"],
    command => "easy_install --upgrade google-api-python-client",
	require => [Package["python-setuptools"] ]
  }

}


include apache
include apache::mod::php
apache::mod { 
	'rewrite': 
}

include php
include mosquitto
include sqlite
include python
