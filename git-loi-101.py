#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
"""
    Usage: git-loi-101.py [--aide] COMMANDE [OPTIONS]
"""
from __future__ import print_function
from __future__ import unicode_literals

import argparse
# import locale
import sys
from subprocess import call, Popen, PIPE, STDOUT
from six import iteritems

try:
    from argcomplete import autocomplete
    autocomplete_installed = True
except ImportError:
    autocomplete_installed = False

# locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')

french_to_english = {
    'clone': 'clone',
    'pousser': 'push',
    'tirer': 'pull',
    'statut': 'status',
    'branche': 'branch',
    'différence': 'diff',
    'initialiser': 'init',
    'étiqueter': 'tag',
    'réinitialiser': 'reset',
    'regarder-ailleurs': 'checkout',
    'afficher': 'show',
    'cachette': 'stash',
    'commettre': 'commit',
    'fusion': 'merge',
    'outil-fusion': 'mergetool',
    'outil-des-différences': 'difftool',
    'cueillette-de-cerise': 'cherry-pick',
    'ajouter': 'add',
    'enlever': 'rm',
    'refonte': 'rebase',
    'rapporter': 'fetch',
    'aide': 'help',
}

french_to_english_flags = {
    'tout': 'all',
    'pruneau': 'prune',
    'émonder': 'prune',
    'dur': 'hard',
    'courge': 'squash',
    'écraser': 'squash',
    'oblige': 'force',
    'récursive': 'r',
}

french_to_english_args = {
    'maître': 'master',
    'tête': 'head',
    'origine': 'origin',
}

parser = argparse.ArgumentParser(description='Wrapper de Git en français', add_help=False)
parser.add_argument('--aide', '-a', action="help")

subparsers = parser.add_subparsers(dest="commandes")

# Git Pull
pull = subparsers.add_parser(
    'tirer',
    help="Mettre à jour l'entrepôt local à partir d'une branche distante",
    add_help=False
)

# Git Push
push = subparsers.add_parser(
    'pousser',
    help="Pousser les changements local ver une branche distante",
    add_help=False
)
push.add_argument('--aide', '-a', action="help")
push.add_argument('distante', nargs='?')
push.add_argument('branche', nargs='?')

# Git Clone
clone = subparsers.add_parser(
    'clone', help="Cloner un entrepôt distante", add_help=False
)
clone.add_argument(
    'entrepôt', help="l'URL de l'entrepôt", metavar="ENTREPÔT"
)
clone.add_argument(
    'dossier', nargs='?', help="Le dossier cible", metavar="DOSSIER"
)

# Git status
status = subparsers.add_parser(
    'statut', help="Voir l'état de l'entrepôt local", add_help=False
)

# Git Branch
branch = subparsers.add_parser(
    'branche', help="Afficher les branches de l'entrepôt", add_help=False
)
branch.add_argument(
    '--tout', '-t', action='store_true', help="Inclus les branches distantes"
)

# Git diff
diff = subparsers.add_parser(
    'différence', help="Compare deux branches", add_help=False
)
diff_tool = subparsers.add_parser(
    'outil-des-différences', help="Compare deux branches", add_help=False
)

init = subparsers.add_parser(
    'initialiser',
    help="Initialiser un entrepôt git dans le dossier actuel",
    add_help=False
)
tag = subparsers.add_parser(
    'étiqueter', help="Ajoute une étiquette sur la branche", add_help=False
)

reset = subparsers.add_parser(
    'réinitialiser', help="Réinitialiser", add_help=False
)
reset.add_argument(
    '--dur', '-d', action='store_true', help="Réinitialiser de manière dur"
)
reset.add_argument(
    'cible', help="Le fichier ou la branche cible", metavar="CIBLE"
)

checkout = subparsers.add_parser('regarder-ailleurs', help="", add_help=False)
show = subparsers.add_parser('afficher', help="", add_help=False)
stash = subparsers.add_parser('cachette', help="", add_help=False)
commit = subparsers.add_parser('commettre', help="", add_help=False)

merge = subparsers.add_parser('fusion', add_help=False)
merge.add_argument(
    '--courge', '-c', action='store_true', help="Fusionner les commit ensemble."
)
merge.add_argument(
    '--écraser', '-e', action='store_true', help="Combiner les commettres ensemble"
)


merge_tool = subparsers.add_parser(
    'outil-fusion',
    help="Gérer les conflits de fusion avec une interface graphique.",
    add_help=False
)

# Git Cherry-Pick
cherry_pick = subparsers.add_parser(
    'cueillette-de-cerise',
    help="Prendre un commis en particulier et l'amener dans la branche actuelle.",
    add_help=False
)

add = subparsers.add_parser('ajouter', add_help=False)
add.add_argument(
    'fichiers', nargs='+', help="Le ou les fichiers à ajouter",
    metavar="FICHIERS",
)
add.add_argument(
    '--oblige', '-o', action='store_true', help="Oblige l'ajout de(s) fichier(s)"
)

rm = subparsers.add_parser('enlever', add_help=False)
rm.add_argument(
    'fichiers', nargs='+', help="Le ou les fichiers à supprimer", metavar="FICHIERS"
)
rm.add_argument(
    '--oblige', '-o', action='store_true', help="Oblige le suppression de(s) fichier(s)"
)
rm.add_argument(
    '--récursive', '-r', action='store_true', help="Fais la suppression de manière récursive"
)

rebase = subparsers.add_parser(
    'refonte',
    help="Mettre à jour l'historique des commis avec une autre branche",
    add_help=False
)
fetch = subparsers.add_parser('rapporter', add_help=False)
fetch.add_argument(
    '--pruneau', '-p', action='store_true', help="Enlever les branches supprimer"
)
fetch.add_argument(
    '--émonder', '-e', action='store_true', help="Enlever les branches supprimer"
)

if autocomplete_installed:
    autocomplete(parser)

args, unknown_args = parser.parse_known_args()

command = french_to_english.get(args.commandes)
if not command:
    if not unknown_args:
        print(__doc__)
        sys.exit(1)
    call(['git'] + unknown_args)
    sys.exit(0)

args = vars(args)
del args['commandes']
git_arguments = ['git', command]

for key, value in iteritems(args):
    if value is True or value is False:
        flag = french_to_english_flags.get(key)
        if flag is True:
            if len(flag) == 1:
                value = "-" + flag
            else:
                value = "--" + flag
        else:
            continue

    if isinstance(value, list):
        if value:
            git_arguments += value

    elif value:
        english_value = french_to_english_args.get(value)
        if english_value:
            value = english_value

        git_arguments.append(value)

all_args = git_arguments + unknown_args

interactive_commands = [
    'commit', 'merge', 'diff'
]

if command in interactive_commands:
    exit_code = call(all_args)
    sys.exit(exit_code)

cmd = None
try:
    cmd = Popen(" ".join(all_args), stdout=PIPE, stderr=STDOUT, shell=True)
    status_code = cmd.wait()
    while True:
        line = cmd.stdout.readline()
        if not line:
            break
        print(line.decode("utf-8"), end='')

    if status_code != 0:
        print("Un erreur est survenu")
        sys.exit(1)

except KeyboardInterrupt:
    if cmd:
        cmd.kill()
