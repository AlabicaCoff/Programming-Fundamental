#include<stdio.h>
#include<conio.h>
#include <time.h>
#include<Windows.h>
#include <thread>

//Global Variables
const int max_bullet = 5;
bool status[max_bullet];
int bx[max_bullet], by[max_bullet];

//Function Declaration
void erase_ship(int x, int y);
void erase_bullet(int x, int y);
void draw_ship(int x, int y);
void draw_bullet(int x, int y);
void gotoxy(int x, int y);
void setcursor(bool visible);
void setcolor(int fg, int bg);

//Main Loop
int main()
{
	clock_t start_t, this_t;
	start_t = clock();
	char ch = ' ';
	int x = 38, y = 20;
	setcursor(0);
	draw_ship(x, y);
	char dir{};
	do {
		this_t = clock();
		if (_kbhit()) {
			ch = _getch();
			if (ch == 'a')
			{
				dir = 'l';
			}
			if (ch == 'd')
			{
				dir = 'r';
			}
			if (ch == 's')
			{
				dir = 'i';
			}

			if (ch == ' ') //Key Shoot
			{
				for (int i = 0; i < max_bullet; i++)
				{
					if (status[i] == 0)
					{
						status[i] = 1;
						bx[i] = x + 2;
						by[i] = y - 1;
						break;
					}
				}
			}
			fflush(stdin);
		}

			if (dir == 'l' && x > 0)
			{
					erase_ship(x, y);
					draw_ship(--x, y);
			}
			if (dir == 'r' && x < 80)
			{
					erase_ship(x, y);
					draw_ship(++x, y);
			}
			if (dir == 'i')
			{
				erase_ship(x, y);
				draw_ship(x, y);
			}
			for (int i = 0; i < max_bullet; i++) //Shoot
			{
				if (status[i] == 1)
				{
					erase_bullet(bx[i], by[i]);
					if (by[i] == 0)
					{
						status[i] = 0;
					}
					else
					{
						draw_bullet(bx[i], --by[i]);
					}
				}
			}
		Sleep(100);

	} while (ch != 'x');
	return 0;
}

//Function Setup
void draw_ship(int x, int y)
{
	setcolor(2, 4);
	gotoxy(x, y);
	printf(" -olo- ");
}

void draw_bullet(int x, int y)
{
	setcolor(4, 0);
	gotoxy(x, y);
	printf(" | ");
}

void gotoxy(int x, int y)
{
	COORD c = { x, y };
	SetConsoleCursorPosition(GetStdHandle(STD_OUTPUT_HANDLE), c);
}

void erase_ship(int x, int y)
{
	setcolor(0, 0);
	gotoxy(x, y);
	printf("       ");
}

void erase_bullet(int x, int y)
{
	setcolor(0, 0);
	gotoxy(x, y);
	printf("   ");
}

void setcursor(bool visible)
{
	HANDLE console = GetStdHandle(STD_OUTPUT_HANDLE);
	CONSOLE_CURSOR_INFO lpCursor;
	lpCursor.bVisible = visible;
	lpCursor.dwSize = 20;
	SetConsoleCursorInfo(console, &lpCursor);
}

void setcolor(int fg, int bg)
{
	HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
	SetConsoleTextAttribute(hConsole, bg * 16 + fg);
}