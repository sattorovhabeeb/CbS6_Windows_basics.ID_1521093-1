/*
    YARA Rule для детектирования file2.bin
    
    Описание: Это правило идентифицирует file2.bin по уникальному SHA256 хешу
*/

rule Detect_File2_Bin
{
    meta:
        description = "Детектирует file2.bin по уникальному SHA256 хешу"
        author = "Habeeb"
        date = "2026-01-03"
        reference = "file2.bin"
        
    strings:
        // Hex-паттерн: начало SHA256 хеша file2
        // 2cc7ce7b82a569fc
        $hex_pattern = { 2c c7 ce 7b 82 a5 69 fc }
        
        // Обычная текстовая строка - версия LFS
        $text_pattern = "version https://git-lfs.github.com/spec/v1" nocase ascii
        
        // Уникальная часть хеша для file2
        // Это средняя часть SHA256, которая отличается от других файлов
        $unique_hash = "a0ce2cbcca35354385a398e8" ascii
        
    condition:
        // Для file2 проверяем:
        // 1. Наличие hex-паттерна (обязательное условие из задания)
        $hex_pattern
        
        // 2. Наличие текстовой строки (обязательное условие из задания)
        and $text_pattern
        
        // 3. Уникальная часть хеша для точной идентификации
        and $unique_hash
        
        // Примечание: здесь НЕ используется условие по размеру,
        // так как оно будет в правиле для file3
}