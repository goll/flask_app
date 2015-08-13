# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  # Define CentOS 7.1 base box
  config.vm.box = "chef/centos-7.1"

  # Forward port 8080 for Flask application
  config.vm.network "forwarded_port", guest: 8080, host: 8080

  # Use VirtualBox provider and increase memory
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "1024"
  end

  # Provision the system using ansible
  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "provisioning/playbook.yml"
  end
end
