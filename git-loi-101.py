#! /usr/bin/python3
# -*- coding: utf-8 -*-
"""
    Usage: git-loi-101.py [--aide] COMMANDE [OPTIONS]
"""
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import locale
import sys
from subprocess import call
from six import iteritems

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
    'émonder': 'prune',
    'dur': 'hard',
    'écraser': 'squash',
    'oblige': 'force',
}

french_to_english_args = {
    'maître': 'master',
    'tête': 'head',
}

parser = argparse.ArgumentParser(description='Wrapper de Git en français', add_help=False)
parser.add_argument('--aide', '-a', action="help")

subparsers = parser.add_subparsers(dest="commandes")

# Git Pull
pull = subparsers.add_parser(
    'tirer',
    help="Mettre à jour l'entrepôt local à partir d'une branche distante",
)

# Git Push
push = subparsers.add_parser(
    'pousser', help="Pousser les changements local ver une branche distante"
)
push.add_argument('distante', nargs='?')
push.add_argument('branche', nargs='?')

# Git Clone
clone = subparsers.add_parser(
    'clone', help="Cloner un entrepôt distante"
)
clone.add_argument(
    'entrepôt', help="l'URL de l'entrepôt", metavar="ENTREPÔT"
)
clone.add_argument(
    'dossier', nargs='?', help="Le dossier cible", metavar="DOSSIER"
)

# Git status
status = subparsers.add_parser(
    'statut', help="Voir l'état de l'entrepôt local"
)

# Git Branch
branch = subparsers.add_parser(
    'branche', help="Afficher les branches de l'entrepôt"
)
branch.add_argument(
    '--tout', '-t', action='store_true', help="Inclus les branches distantes"
)

# Git diff
diff = subparsers.add_parser('différence', help="Compare deux branches")
diff_tool = subparsers.add_parser(
    'outil-des-différences', help="Compare deux branches"
)

init = subparsers.add_parser(
    'initialiser', help="Initialiser un entrepôt git dans le dossier actuel"
)
tag = subparsers.add_parser('étiqueter', help="Ajoute une étiquette sur la branche")

reset = subparsers.add_parser('réinitialiser', help="Réinitialiser")
reset.add_argument(
    '--dur', '-d', action='store_true', help="Réinitialiser de manière dur"
)
reset.add_argument(
    'cible', help="Le fichier ou la branche cible", metavar="CIBLE"
)

checkout = subparsers.add_parser('regarder-ailleurs', help="")
show = subparsers.add_parser('afficher', help="")
stash = subparsers.add_parser('cachette', help="")
commit = subparsers.add_parser('commettre', help="")

merge = subparsers.add_parser('fusion')
merge.add_argument(
    '--écraser', '-c', action='store_true', help="Combiner les commettres ensemble"
)

merge_tool = subparsers.add_parser('outil-fusion')

# Git Cherry-Pick
cherry_pick = subparsers.add_parser('cueillette-de-cerise')

add = subparsers.add_parser('ajouter')
add.add_argument(
    'fichiers', nargs='+', help="Le ou les fichiers", metavar="FICHIERS"
)

rm = subparsers.add_parser('enlever')

rebase = subparsers.add_parser('refonte')
fetch = subparsers.add_parser('rapporter')
fetch.add_argument(
    '--émonder', '-p', action='store_true', help="Enlever les branches supprimer"
)

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
        if flag:
            value = "--" + flag

    if isinstance(value, list):
        if value:
            git_arguments += value

    elif value:
        english_value = french_to_english_args.get(value)
        if english_value:
            value = english_value

        git_arguments.append(value)

call(git_arguments + unknown_args)
