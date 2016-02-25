ENTRY(start)
SECTIONS {
    . = 1M

    .boot :
    {
        /* ensure that the multoboot header is at the beginning */
        *(.multoboot_header)
    }

    .text :
    {
        *(.text)
    }
}

