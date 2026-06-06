┌———————————————————————————————————————————————————————————————————————————┐
│   ooooo      ooo ooooooooooooo oooooo     oooo oooooooooooo  .oooooo..o   │
│   `888b.     `8' 8'   888   `8  `888.     .8'  `888'     `8 d8P'    `Y8   │
│    8 `88b.    8       888        `888.   .8'    888         Y88bo.        │
│    8   `88b.  8       888         `888. .8'     888oooo8     `"Y8888o.    │
│    8     `88b.8       888          `888.8'      888    "         `"Y88b   │
│    8       `888       888           `888'       888         oo     .d8P   │
│   o8o        `8      o888o           `8'       o888o        8""88888P'    │
├—————————————————————————————————————————————┬—————————————————————————————┤
│  </ Nuclearity, The Virtual FileSystem. />  │"The Guide"; The "FileSystem"│
├—————————————————————————————————————————————┴—————————————————————————————┤
│ <# Once you understand the FileSystem, It'll give you even more than you  │
│ could think it'll give by understanding it #> Yet Unknownn for me Author  │
└———————————————————————————————————————————————————————————————————————————┘



|======================================================================|
|>                               GROUP                  TOTAL_SIZE    <|
|——————————————————————————————————————————————————————————————————————|———————————————|   
|      NAME        |          DESCRIPTION          |       SIZE        |    DATATYPE   |   |======[  TOPIC  ]======|
|                  |                               |                   |               |———| Remark for this topic |
|======================================================================|===============|   |=======================|



|======================================================================|                   |======[ DT size ]======|
|>                              HEADER                    8 bytes     <|                 ┌—| Entire DataTable size |
|——————————————————————————————————————————————————————————————————————|———————————————| │ |=======================|
|      MAGIC       | NUFS |  NuclearityFileSystem  |      4 bytes      | s    CHAR     | │ 
|  datatable_size  | Size of the entire DATATABLE  |      4 bytes      | L  ULONG INT  |—┘ |======[ SEC_SIZE ]======|
|                  |                               |                   |               |   | Size of individual     |
|=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-|-=-=-=-=-=-=-=-| ┌—| data sector containing |
|>                        DATA_TABLE_SECTOR              12+ bytes    <|                 │ | file-related data.     |
|——————————————————————————————————————————————————————————————————————|———————————————| │ |========================|
|   size_offset    |   Sector size sector offset   |      2 byte       | H  USHORT INT | │
|   sector_size    |       Sector Size data        |   set by offset   | I   U INT     |—┘ |======[ FILE ID ]======|
|    id_offset     |     File ID sector offset     |      2 byte       | H  USHORT INT |   | SHA-xxx generated ID  |
|     file_id      |      File ID sector data      |   set by offset   | s     CHAR    |———| using the in-game     |   |======[ LOCATION ]======|
|  location_offset |  File location sector offset  |      2 byte       | H  USHORT INT |   | date and time.      ;)|   | File location, based   |
|     location     |   Actual file location data   |   set by offset   | L  ULONG INT  |——┐|=======================|┌——| on byte offset from    |
|   name_offset    |    File name sector offset    |      2 byte       | H  USHORT INT |  └—————————————————————————┘  | the end of DATA_TABLE  |
|    file_name     |        File name data         |   set by offset   | s     CHAR    |   |======[ METADATA ]======|  |========================|
| metadata_offset  |  Offset of te metadata block  |      4 bytes      | I    U INT    |   | Metadata represents a  |
|     metadata     |     Metadata block itself     |   set by offset   | s     CHAR    |———| json dictionary with   |
|                  |                               |                   |               |   | any text in it.        |
|=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-|-=-=-=-=-=-=-=-|   |========================|
|>                           DATA_BLOCKS                 4+ bytes     <|
|——————————————————————————————————————————————————————————————————————|———————————————|
|   data_offset    |       Data block offset       |      4 bytes      | L  ULONG INT  |
|       data       |        Data block data        |   set by offset   | —  RAW BYTES  |
|                  |                               |                   |               |
|======================================================================|===============|
