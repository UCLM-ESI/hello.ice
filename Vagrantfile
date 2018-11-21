# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.provider :virtualbox do |vb|
    vb.memory = 4096
    vb.cpus = 2
  end

  config.vm.define "ice36" do |node|
    node.vm.box = "debian/contrib-stretch64" 
    node.vm.hostname = "ice36"
    node.vm.provision "ansible" do |ansible|
      ansible.verbose = "v"
      ansible.playbook = "playbook-ice36.yml"
    end
  end

  config.vm.define "ice37" do |node|
    node.vm.box = "debian/contrib-testing64" 
    node.vm.hostname = "ice37"
    node.vm.provision "ansible" do |ansible|
      ansible.verbose = "v"
      ansible.playbook = "playbook-ice37.yml"
    end
  end

end
