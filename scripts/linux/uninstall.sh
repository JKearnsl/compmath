#!/bin/sh

set -e

# Variables
PROGRAM_NAME='CompMath'
PROGRAM_NAME_LOWER=$(echo "$PROGRAM_NAME" | tr '[:upper:]' '[:lower:]')

INSTALL_PATH=/opt/$PROGRAM_NAME_LOWER
ICON_PATH="/usr/share/icons/hicolor"


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

trap 'echo "$RED$BOLDВозникла ошибка при удалении программы $PROGRAM_NAME$ENDCOLOR"' EXIT

log info "Удаление программы $PROGRAM_NAME"

if [ "$(id -u)" -ne 0 ]; then
  log error "Этот скрипт должен быть запущен с правами суперпользователя."
  exit 1
fi

# Remove app
rm -rf "${INSTALL_PATH:?}/"

# Remove files
getent passwd | while IFS=: read -r _ _ uid _ _ home _; do
  if [ "$uid" -ge 1000 ] && [ -d "$home" ]; then
    rm -rf "${home:?}/.$PROGRAM_NAME_LOWER"
  fi
done

# Remove executable
rm -f /usr/local/bin/"$PROGRAM_NAME_LOWER"

# Remove .desktop file
rm -f /usr/share/applications/"$PROGRAM_NAME_LOWER".desktop
update-desktop-database /usr/share/applications

# Remove icon
rm -f "$ICON_PATH"/64x64/apps/"$PROGRAM_NAME_LOWER".png
rm -f "$ICON_PATH"/128x128/apps/"$PROGRAM_NAME_LOWER".png
rm -f "$ICON_PATH"/256x256/apps/"$PROGRAM_NAME_LOWER".png

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

log info 'Удаление успешно завершено.'

trap - EXIT
