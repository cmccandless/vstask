from .cli import completable, terminal

COMPLETION = """#!/bin/bash
_vstask()
{
    local cur prev opts base
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    flags=\"""" + ' '.join(completable()) + """\"

    case "${prev}" in
        """ + '|'.join(terminal()) + """) COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) ) ;;
        *)
            opts="$(${COMP_WORDS[*]} -l)"
            COMPREPLY=( $(compgen -W "${flags} ${opts}" -- ${cur}) )
        ;;
    esac
}
complete -F _vstask vstask
"""
