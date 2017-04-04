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
  config.vm.network "forwarded_port", guest: 8080, host: 8080, host_ip: "127.0.0.1"

  # This allows the project files to appear in the virtual machine,
  # located at the directory '/home/vagrant/csmodify'.
  config.vm.synced_folder ".", "/home/vagrant/csmodify"

  # Enable provisioning with a shell script, which can be found in
  # 'vagrant_setup/bootstrap.sh'.
  config.vm.provision :shell, :path => "vagrant_setup/bootstrap.sh"
end
