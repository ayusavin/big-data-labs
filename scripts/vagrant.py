from scripts.base import PoetryShellScript


class VagrantUpScript(PoetryShellScript):
    command = "vagrant up --provider=libvirt"


class VagrantDownScript(PoetryShellScript):
    command = "vagrant destroy -f"
