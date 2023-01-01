#include<stdio.h>
#include<conio.h>
#include<Windows.h>
//Function Declaration
void erase_ship(int x, int y);
void draw_ship(int x, int y);
void gotoxy(int x, int y);
//Main Loop
int main()
{
	char ch = ' ';
	int x = 38, y = 20;
	draw_ship(x, y);
	do {
		if (_kbhit()) {
			ch = _getch();
			if (ch == 'a')
			{
				if (x > 0)
				{
					draw_ship(--x, y);
				}
			}
			if (ch == 'd')
			{
				if (x < 80)
				{
					draw_ship(++x, y);
				}
			}
			if (ch == 'w')
			{
				if (y > 0)
				{
					erase_ship(x, y);
					draw_ship(x, --y);
				}
			}
			if (ch == 's')
			{
				erase_ship(x, y);
				draw_ship(x, ++y);
			}
			fflush(stdin);
		}
		Sleep(100);
	} while (ch != 'x');
	return 0;
}
//Function Setup
void draw_ship(int x, int y)
{
	gotoxy(x, y);
	printf(" <-0-> ");
}
void gotoxy(int x, int y)
{
	COORD c = { x, y };
	SetConsoleCursorPosition(GetStdHandle(STD_OUTPUT_HANDLE), c);
}
void erase_ship(int x, int y)
{
	gotoxy(x, y);
	printf("       ");}