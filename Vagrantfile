# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://atlas.hashicorp.com/search.
  config.vm.box = "hashicorp/precise64"

  # By default, running 'python app.py' will create a server for the app,
  # which can be accessed at localhost:8080.
  # 
  # Therefore, We specify a guest port number that is not 80 to
  # avoid conflicting with the Python app.
  config.vm.network "forwarded_port", guest: 8080, host: 8080

  # This allows the project files to appear in the virtual machine,
  # located at the directory '/vagrant'.
  config.vm.synced_folder ".", "/vagrant"

  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.
  config.vm.provision :shell, :path => "vagrant_setup/bootstrap.sh"
end
