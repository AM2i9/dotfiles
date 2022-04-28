
dir=~/dotfiles

for file in $(ls $dir/system | grep -v /); do
    if [[ "$file" != "install.sh" ]]; then
    echo "Creating symlink to $file in home directory."
    ln -s $dir/system/$file ~/.$file
    fi
done

install_zsh () {
    if [ -f /bin/zsh -o -f /usr/bin/zsh ]; then
        if [[ ! -d ~/.oh-my-zsh/ ]]; then
            git clone http://github.com/robbyrussell/oh-my-zsh.git ~/.oh-my-zsh
        fi
        if [[ ! $(echo $SHELL) == $(which zsh) ]]; then
            chsh -s $(which zsh)
        fi
    else
        platform=$(uname);
        if [[ $platform == 'Linux' ]]; then
            if [[ -f /etc/arch-release ]]; then
                sudo pacman -S zsh
                install_zsh
            fi
            if [[ -f /etc/debian_version ]]; then
                sudo apt-get install zsh
                install_zsh
            fi
        else
            echo "Please install zsh, then re-run this script!"
            exit
        fi
    fi
}

install_zsh
