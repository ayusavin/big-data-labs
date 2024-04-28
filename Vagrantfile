nodes = [
    {
        :name => "master-node",
        :eth1 => "192.168.56.3",
        :mem => "1600",
        :cpu => "2"
    },
    {
        :name => "worker-node",
        :eth1 => "192.168.56.5",
        :mem => "4096",
        :cpu => "3"
    }
  ]

Vagrant.configure(2) do |config|
    config.vm.box = "debian/bookworm64"
    config.vm.synced_folder ".", "/vagrant", id: "vagrant-root", disabled: true
    

    config.vm.provision "shell" do |s|
        ssh_pub_key = File.readlines("#{Dir.home}/.ssh/id_rsa.pub").first.strip
        s.inline = <<-SHELL
          echo #{ssh_pub_key} >> /home/vagrant/.ssh/authorized_keys
          echo #{ssh_pub_key} >> /root/.ssh/authorized_keys
        SHELL
      end

    nodes.each do |opts|
        config.vm.define opts[:name] do |config|
          config.vm.hostname = opts[:name]
          config.vm.provider :libvirt do |v|
            v.driver = "kvm"
            v.cpus = opts[:cpu]
            v.memory = opts[:mem]
          end
    
          config.vm.network :private_network, ip: opts[:eth1]
        end
      end
end
