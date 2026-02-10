/*
    YARA Rule для детектирования file1.bin
    
    Описание: Это правило идентифицирует file1.bin по уникальному SHA256 хешу
    и размеру файла
*/

rule Detect_File1_Bin
{
    meta:
        description = "Детектирует file1.bin по уникальному SHA256 хешу и размеру"
        author = "Security Analyst"
        date = "2026-01-03"
        reference = "file1.bin"
        
    strings:
        
        $hex_pattern = { cb d0 00 c0 44 bf 9d 3d }
        
         $text_pattern = "git-lfs.github.com" nocase ascii
        
         $unique_hash = "6e0688bae226abeae8eb78e1" ascii
        
    condition:
        // 1. Размер файла должен быть точно 1000027 байт
        filesize == 1000027
        
        // 2. Должна присутствовать hex-строка
        and $hex_pattern
        
        // 3. Должна присутствовать текстовая строка
        and $text_pattern
        
        // 4. Должна присутствовать уникальная часть хеша
        and $unique_hash
}