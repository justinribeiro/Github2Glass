Vagrant::Config.run do |config|
  config.vm.box = "precise64"
  config.vm.forward_port 80, 4040
  config.vm.provision :shell, :inline => "apt-get update --fix-missing"
  config.vm.provision :puppet, :module_path => "modules"
end
