#!/bin/bash


# Instalar brew
BREW_INSTALLED=$(which brew)
if [ -z $BREW_INSTALLED ]; then
    echo "Install brew..."
    ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
else
    echo "Brew estaba instalado"
fi


# Instalar node
NODE_INSTALLED=$(which npm)
if [ -z NODE_INSTALLED ]; then
    echo "Install npm..."
    brew install npm
else
    echo "Node estaba instalado"
fi


# Instalar bower
BOWER_INSTALLED=$(npm list -g | grep bower)
if [ -z BOWER_INSTALLED ]; then
    echo "Install bower..."
    npm install -g bower
else
    echo "bower estaba instalado"
fi

# Instalar los requirements del proyecto
echo "Install requirements..."
pip install -r requirements.txt


