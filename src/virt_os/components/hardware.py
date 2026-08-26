from dataclasses import dataclass, field


@dataclass
class CPU:
    present:    bool            = True
    model:      str             = "SCaPM.748"                   # Static Calculating and Predicting Machine -- v0748
    cores:      int             = 1
    speed:      int             = 600                           # mHz


@dataclass
class RAM:
    speed:      int             = 100                           # mHz
    total:      int             = 196_608                       # ━┓        |   192 MiB |   (3x64 MiB)
    used:       int             = 0                             #  ┃ KiB    |   0   MiB
    reserved:   int             = 2048                          # ━┛        |   2   MiB

    @property
    def free(self):
        return  self.total - self.reserved - self.used


@dataclass
class NTVS:
    
    structure:  dict            = {
        "header":       [               # DATA  |      DESCRIPRION      |     SIZE      |
            'NUFS',                     # MAGIC | NUclearityFileSystem. |   4 bytes     |
            '00000',                    #       |                       |               |
            '00000',                    #       |                       |               |
            '00000'                     #       |                       |               |
        ],
        "data_table":   [
            'id_offset',                #       |                       |               |
            'file_id',                  #       |                       | set by offset |
            'pos_offset',               #       |                       |               |
            'file_pos',                 #       |                       | set by offset |
            'name_offset',              #       |                       |               |
            'file_name'                 #       |                       | set by offset |
        ],
        "data_block":   [[
            'offset',                   #       |                       |               |
            'data'                      #       |                       | set by offset |
        ]]
    }


@dataclass
class FileSystem:
    variation:  NTVS            = field(default_factory=NTVS)


@dataclass
class Partition:
    label:      str             = "Data Drive"
    size:       int             = 9_404_416                     # KiB       |  ~9 GiB   |   32 MiB left for Boot.
    used:       int             = 0

    @property
    def free(self):
        return  self.size - self.used


@dataclass
class Disk:
    variation:  str             = "HDD | NASSD 3/4"             # Nuclear Albino SubSystem Drive v3 Gen4
    total:      int             = 9_437_184                     # KiB       |   9 GiB
    partitions: list[Partition] = field(default_factory=list)

    @property
    def used(self):
        mem = 0
        for part in self.partitions:
            mem += part.used
        return mem 

    @property
    def free(self):
        mem = 0
        for part in self.partitions:
            mem += part.free
        
        return mem


@dataclass
class Hardware:
    cpu:        CPU             = field(default_factory=CPU)
    cpu_num:    int             = 2                             # amount of CPUs on the MotherBoard
    ram:        RAM             = field(default_factory=RAM)
    disks:      list[Disk]      = field(default_factory=list)   