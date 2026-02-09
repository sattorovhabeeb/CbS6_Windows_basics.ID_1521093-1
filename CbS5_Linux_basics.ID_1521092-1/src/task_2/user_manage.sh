#!/bin/bash


echo "=== Создание пользователей и групп ==="


echo "1. Создание пользователя user и группы default_users..."


groupadd default_users
echo "   - Создана группа default_users"

useradd -m -g default_users user
echo "   - Создан пользователь user в группе default_users"

echo "2. Создание секретных пользователей..."

groupadd secret_users
echo "   - Создана группа secret_users"

useradd -m -g secret_users secret_agent
useradd -m -g secret_users secret_spy
useradd -m -g secret_users secret_boss
echo "   - Созданы пользователи: secret_agent, secret_spy, secret_boss"

echo "3. Настройка прав доступа для домашних директорий secret_users..."

chmod 770 /home/secret_agent
chmod 770 /home/secret_spy  
chmod 770 /home/secret_boss
echo "   - Установлены права 770 для домашних директорий secret_users"
echo "   - Только пользователи группы secret_users могут получать доступ друг к другу"

echo "4. Настройка прав доступа для /var..."

chmod 777 /var
echo "   - Установлены права 777 для /var (доступ для всех)"

echo "5. Установка apache2..."

apt update -qq

apt install -y apache2
echo "   - Apache2 установлен"

echo "   - Проверка статуса apache2:"
systemctl status apache2 --no-pager -l

echo "6. Настройка sudo для группы default_users..."


echo "%default_users ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
echo "   - Группа default_users может выполнять sudo команды без пароля"

echo ""
echo "=== ЗАВЕРШЕНО ==="
