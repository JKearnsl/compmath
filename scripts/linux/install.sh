#!/bin/sh

set -e

# Variables
SCRIPT_DIR=$(dirname "$0")

PROGRAM_NAME='CompMath'
PROGRAM_NAME_LOWER=$(echo "$PROGRAM_NAME" | tr '[:upper:]' '[:lower:]')
PROGRAM_PATH=$SCRIPT_DIR/../../src
CONFIG_PATH=$SCRIPT_DIR/../../config.ini
EXECUTABLE_PATH="${SCRIPT_DIR}/${PROGRAM_NAME_LOWER}.sh"
UNINSTALL_SCRIPT_PATH="${SCRIPT_DIR}/uninstall.sh"
PROGRAM_ASSET_PATH=$PROGRAM_PATH/$PROGRAM_NAME_LOWER/assets
DESKTOP_FILE_PATH=$SCRIPT_DIR/.desktop
PYTHON_VERSION=3.12

INSTALL_PATH=/opt/$PROGRAM_NAME_LOWER
ICON_PATH=/usr/share/icons/hicolor

# Color map
RED=$(tput setaf 1)
GREEN=$(tput setaf 2)
YELLOW=$(tput setaf 3)
BOLD=$(tput bold)
ENDCOLOR=$(tput sgr0)

log() {
  if [ "$1" = "info" ]; then
    echo "$BOLD$GREEN$2$ENDCOLOR"
  elif [ "$1" = "error" ]; then
    echo "${BOLD}${RED}Ошибка: $2${ENDCOLOR}" >&2
  elif [ "$1" = "warning" ]; then
    echo "$BOLD$YELLOW$2$ENDCOLOR"
  fi
}

trap 'echo "$RED$BOLDВозникла ошибка при установке программы $PROGRAM_NAME$ENDCOLOR"' EXIT



log info 'Установка программы '$PROGRAM_NAME

if [ "$(id -u)" -ne 0 ]; then
  log error "Этот скрипт должен быть запущен с правами суперпользователя."
  exit 1
fi

# Check if python3.12 is installed
if ! [ -x "$(command -v python$PYTHON_VERSION)" ]; then
  log warning 'Внимание: python'$PYTHON_VERSION' не установлен.'

  # Install python$PYTHON_VERSION
  log info 'Установка python'$PYTHON_VERSION'...'
  if [ -x "$(command -v apt)" ]; then
    apt install python$PYTHON_VERSION
  elif [ -x "$(command -v pacman)" ]; then
    pacman -S python$PYTHON_VERSION
  elif [ -x "$(command -v dnf)" ]; then
    dnf install python$PYTHON_VERSION
  elif [ -x "$(command -v zypper)" ]; then
    zypper install python$PYTHON_VERSION
  elif [ -x "$(command -v xbps-install)" ]; then
    xbps-install -S python$PYTHON_VERSION
  elif [ -x "$(command -v eopkg)" ]; then
    eopkg install python$PYTHON_VERSION
  elif [ -x "$(command -v emerge)" ]; then
    emerge -av python$PYTHON_VERSION
  elif [ -x "$(command -v pkg)" ]; then
    pkg install python$PYTHON_VERSION
  elif [ -x "$(command -v apk)" ]; then
    apk add python$PYTHON_VERSION
  elif [ -x "$(command -v swupd)" ]; then
    swupd bundle-add python$PYTHON_VERSION
  elif [ -x "$(command -v tazpkg)" ]; then
    tazpkg get-install python$PYTHON_VERSION
  elif [ -x "$(command -v guix)" ]; then
    guix install python$PYTHON_VERSION
  elif [ -x "$(command -v nix-env)" ]; then
    nix-env -i python$PYTHON_VERSION
  elif [ -x "$(command -v brew)" ]; then
    brew install python$PYTHON_VERSION
  elif [ -x "$(command -v yay)" ]; then
    yay -S python$PYTHON_VERSION
  elif [ -x "$(command -v snap)" ]; then
    snap install python$PYTHON_VERSION
  elif [ -x "$(command -v flatpak)" ]; then
    flatpak install python$PYTHON_VERSION
  elif [ -x "$(command -v termux)" ]; then
    pkg install python$PYTHON_VERSION
  elif [ -x "$(command -v pkg_add)" ]; then
    pkg_add python$PYTHON_VERSION
  elif [ -x "$(command -v kcp)" ]; then
    kcp -i python$PYTHON_VERSION
  else
    log error "Не удалось установить python$PYTHON_VERSION
    Пожалуйста, установите python$PYTHON_VERSION вручную и повторите попытку"
    exit 1
  fi
fi

# Install icon
cp "$PROGRAM_ASSET_PATH"/icons/logo-64.png "$ICON_PATH"/64x64/apps/"$PROGRAM_NAME_LOWER".png
cp "$PROGRAM_ASSET_PATH"/icons/logo-128.png "$ICON_PATH"/128x128/apps/"$PROGRAM_NAME_LOWER".png
cp "$PROGRAM_ASSET_PATH"/icons/logo-256.png "$ICON_PATH"/256x256/apps/"$PROGRAM_NAME_LOWER".png

# Install .desktop file
cp "$DESKTOP_FILE_PATH" /usr/share/applications/"$PROGRAM_NAME_LOWER".desktop
update-desktop-database /usr/share/applications

# Install app
log info 'Установка приложения...'

cp -r "$PROGRAM_PATH" "$INSTALL_PATH"/


# Create config file
getent passwd | while IFS=: read -r username _ uid _ _ home _; do
  if [ "$uid" -ge 1000 ] && [ -d "$home" ]; then
    mkdir -p "$home/.$PROGRAM_NAME_LOWER"
    cp "$CONFIG_PATH" "$home/.$PROGRAM_NAME_LOWER/config.ini"
    chown -R "$username":"$username" "$home/.$PROGRAM_NAME_LOWER"
  fi
done

# Create uninstall script
cp "$UNINSTALL_SCRIPT_PATH" "$INSTALL_PATH"/
chmod +x "$INSTALL_PATH"/uninstall.sh

# Make executable
cp "$EXECUTABLE_PATH" "$INSTALL_PATH"/
chmod +x "${INSTALL_PATH}/${PROGRAM_NAME_LOWER}.sh"
ln -sf "${INSTALL_PATH}/${PROGRAM_NAME_LOWER}.sh" "/usr/local/bin/${PROGRAM_NAME_LOWER}"
chmod +x "/usr/local/bin/${PROGRAM_NAME_LOWER}"

# Install dependencies for app
python$PYTHON_VERSION -m venv "$INSTALL_PATH"/venv
. "$INSTALL_PATH"/venv/bin/activate
pip install -e .

# Update icon cache
# GNOME
if [ -x "$(command -v gtk-update-icon-cache)" ]; then
    log info "Обновление кэша иконок GNOME..."
    gtk-update-icon-cache -f -t "$ICON_PATH"/
fi

# KDE
if [ -x "$(command -v kbuildsycoca5)" ]; then
    log info "Обновление кэша иконок KDE..."
    kbuildsycoca5 --noincremental
fi

# XFCE
if [ -x "$(command -v xfce4-panel)" ]; then
    log info "Обновление кэша иконок XFCE..."
    xfce4-panel --restart
fi

# LXDE
if [ -x "$(command -v lxpanelctl)" ]; then
    log info "Обновление кэша иконок LXDE..."
    lxpanelctl restart
fi

# MATE
if [ -x "$(command -v mate-panel)" ]; then
    log info "Обновление кэша иконок MATE..."
    mate-panel --replace &
fi

log info "Обновление кэша иконок завершено."

log info 'Установка успешно завершена.'
log info "Приложение было установлено в $INSTALL_PATH"
log info "Вы можете удалить приложение выполнив: $INSTALL_PATH/install/linux/uninstall.sh"

trap - EXIT
