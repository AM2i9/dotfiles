
dir=~/dotfiles

for file in $(ls $dir/system | grep -v /); do
    if [[ "$file" != "install.sh" ]]; then
    echo "Creating symlink to $file in home directory."
    ln -sf $dir/system/$file ~/.$file
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

echo "Using i3 (gaps)? [N\y]"
read usingithree

if [[ ${usingithree^^} == 'Y' ]]; then
    echo "Linking i3, picom, and rofi configs..."
    ln -sf $dir/i3 ~/.config
    ln -sf $dir/picom ~/.config
    ln -sf $dir/rofi ~/.config
    ln -sf $dir/dunst ~/.config
    ln -sf $dir/betterlockscreenrc ~/.config
    ln -sf $dir/kitty ~/.config
    
    echo "Installing dunst and rofi"
    if [[ -f /etc/arch-release ]]; then
        sudo pacman -S dunst rofi picom
    fi
    if [[ -f /etc/debian_version ]]; then
	sudo apt-get install dunst rofi picom
    fi

    echo "Installing bumblebee-status..."
    python -m pip install bumblebee-status=="2.1.5"

    echo "Installing betterlockscreen..."
    wget https://git.io/JZyxV -O - -q | bash -- system latest true
fi

echo "Configuration complete"
