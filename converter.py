# -*- encoding: utf-8 -*-

import os
import sys
from string import Template

# Output type: document, part of document
output_complete_doc = False

document_block = """
\\documentclass{scrreprt}
\\usepackage[utf8]{inputenc}
\\usepackage[catalan]{babel}

\\usepackage{listings}
\\lstset{
  basicstyle=\\sffamily,
}

\\newcommand{\\code}[1]{\\texttt{#1}}
\\newcommand{\\bfcode}[1]{{\\large\code{\\textbf{#1}}}}
\\newcommand{\\comanda}[3]{\\code{#1.}\\bfcode{#2}\\code{(}\\textit{#3}\\code{)}}

\\newcommand{\\atribut}[3]{\\item[#1](\\textit{#2}) -- #3}

\\DeclareFontShape{OT1}{cmtt}{bx}{n}{<5><6><7><8><9><10><10.95><12><14.4><17.28><20.74><24.88>cmttb10}{}

\\begin{document}
$content
\\end{document}
"""

command_block = """
$command

$desc_block

$args_ret

$code_block

"""


def comment2tex(lines, module=None, function=None):
    titol = []
    subtitol = []
    for n_line in range(0, len(lines)):
        if '===' in lines[n_line]:
            titol.append(n_line)
        elif '---' in lines[n_line]:
            subtitol.append(n_line)

    simple_args = ""
    desc = ""
    args = ""
    arg = "  \\atribut{$arg_name}{$arg_type}{$arg_desc}\n"
    ret = ""
    code = ""

    args_list = []
    code_line = None
    for n_line in range(0, len(lines)):
        if not code_line:
            if n_line in titol or n_line in subtitol:
                continue
            elif n_line + 1 in titol:
                desc += '\\section{' + lines[n_line].lstrip().replace('\n', '') + '}\n'
            elif n_line + 1 in subtitol:
                desc += '\\subsection{' + lines[n_line].lstrip().replace('\n', '') + '}\n'
            elif ':param' in lines[n_line]:
                line = lines[n_line].split(':')
                arg_name = line[-2].split(' ')[-1].lstrip().replace('\n', '')
                arg_type = line[-2].split(' ')[-2].lstrip().replace('\n', '')
                arg_desc = line[-1].lstrip().replace('\n', '')
                args_list.append(arg_name)
                args += Template(arg).substitute(arg_name=arg_name, arg_type=arg_type, arg_desc=arg_desc)
            elif ':rtype' in lines[n_line]:
                ret = lines[n_line].split(':')[-1].lstrip().replace('\n', '')
            elif ">>>" in lines[n_line]:
                code_line = n_line
                break
            else:
                if lines[n_line].lstrip() == '\n':
                    desc += '\\\\'
                else:
                    desc += lines[n_line]

    code_block = ''
    if code_line:
        code = ' '.join(lines[code_line:])
        if code:
            code_block = """\\begin{lstlisting}[language=python]
$code
\\end{lstlisting}
"""
        code_block = Template(code_block).substitute(code=code)

    simple_args = ', '.join(args_list)

    command = ''
    if function:
        command = "\\comanda{$module}{$function}{$simple_args}\n"
        command = Template(command).substitute(module=module, function=function, simple_args=simple_args)

    desc_block = '$desc'
    if function:
        desc_block = """\\begin{quote}
$desc
\\end{quote}
"""
    desc_block = Template(desc_block).substitute(desc=desc)

    args_ret = ''
    if args and ret:
        args_ret = """\\begin{quote}
\\begin{description}
$parametres
$return_type
\\end{quote}
"""
        parametres = ''
        if args:
            parametres = """\\item[Parametres] \\leavevmode
  \\begin{description}
  $args
  \\end{description}
"""
            parametres = Template(parametres).substitute(args=args)

        return_type = ''
        if ret:
            return_type = """\\item[{Return type}] \\leavevmode
  \\begin{description}
  \\item[$ret]
  \\end{description}
\\end{description}
"""
            return_type = Template(return_type).substitute(ret=ret)

        args_ret = Template(args_ret).substitute(parametres=parametres, return_type=return_type)

    return Template(command_block).substitute(command=command, desc_block=desc_block, args_ret=args_ret, code_block=code_block)

if __name__ == '__main__':
    module = str(sys.argv[1])
    if module[-3:] == '.py':
        f = open(module, 'r')
        module = module.replace('.py', '')
    else:
        f = open(module + '.py', 'r')
    lines = f.readlines()
    f.close()

    comments = []
    functions = []
    in_comment = False
    comment = [None, None]
    for n_line in range(len(lines)):
        if not in_comment:
            if '"""' in lines[n_line]:
                in_comment = True
                comment[0] = n_line
            elif 'def ' in lines[n_line]:
                functions.append(n_line)
        else:
            if '"""' in lines[n_line]:
                in_comment = False
                comment[1] = n_line
                comments.append(comment)
                comment = [None, None]

    content = ''
    for init_comment, end_comment in comments:
        if init_comment - 1 in functions:
            function_name = lines[init_comment - 1].split('def ')[-1].split('(')[0]
            content += comment2tex(lines[init_comment + 1: end_comment], module, function_name)
        else:
            content += comment2tex(lines[init_comment + 1: end_comment], False, False)
    content = content.replace('_', '\_')

    if output_complete_doc:
        document = Template(document_block).substitute(content=content)
    else:
        document = content

    if not os.path.isdir('./doc'):
        os.makedirs('./doc')

    f = open('./doc/doc-' + module + '.tex', 'w')
    f.write(document)
    f.close()
