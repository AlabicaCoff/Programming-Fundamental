#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>
#include<conio.h>
#include <time.h>
#include<Windows.h>
#include <thread>

//Global Variables
bool status[5];
int bx[5], by[5];
int sx, sy;

//Function Declaration
void draw_courtX(int x, int y);
void draw_courtY(int x, int y);
void erase_ship(int x, int y);
void erase_bullet(int x, int y);
void draw_ship(int x, int y);
void draw_bullet(int x, int y);
void draw_star(int x, int y);
void gotoxy(int x, int y);
void setcursor(bool visible);
void setcolor(int fg, int bg);
char cursor(int x, int y);
void score(int z, int x, int y);

//Main Loop
int main()
{
	char ch = ' ';
	char dir{};
	int x = 38, y = 20, hit = 0, point = 0;;
	setcursor(0);
	draw_ship(x, y);
	srand(time(NULL));
	for (int i = 0; i <= 20; i++)
	{
		draw_courtX(79, i);
	}
	for (int i = 0; i <= 80; i++)
	{
		draw_courtY(i, 21);
	}
	for (int i = 0; i < 20; i++)
	{
		sx = 10 + rand() % 61;
		sy = 2 + rand() % 4;
		draw_star(sx, sy);
	}

	do {
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
				for (int i = 0; i < 5; i++)
				{
					if (status[i] == 0)
					{
						status[i] = 1;
						bx[i] = x + 3;
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
		if (dir == 'r' && x < 70)
		{
				erase_ship(x, y);
				draw_ship(++x, y);
		}
		if (dir == 'i')
		{
			erase_ship(x, y);
			draw_ship(x, y);
		}
		for (int i = 0; i < 5; i++) //Shoot
		{
			if (status[i] == 1)
			{
				std::thread p(Beep, 600, 200);
				p.detach();
				erase_bullet(bx[i], by[i]);
				if (by[i] == 0)
				{
					status[i] = 0;
				}
				else
				{
					if (cursor(bx[i], by[i] - 1) == '*')
					{
						hit = 1;
					}
					draw_bullet(bx[i], --by[i]);
				}
				if (hit)
				{
					point += 1;
					erase_bullet(bx[i], by[i]);
					std::thread p(Beep, 700, 200);
					p.detach();
					hit = 0;
					status[i] = 0;
					sx = 10 + rand() % 61;
					sy = 2 + rand() % 4;
					draw_star(sx, sy);
				}
			}
		}
		score(point, 77, 0);
		Sleep(100);

	} while (ch != 'x');
	return 0;
}

//Function Setup
void draw_courtX(int x, int y)
{
	setcolor(7, 0);
	gotoxy(x, y);
	printf("||");
}

void draw_courtY(int x, int y)
{
	setcolor(7, 0);
	gotoxy(x, y);
	printf("=");
}

void draw_ship(int x, int y)
{
	setcolor(2, 4);
	gotoxy(x, y);
	printf(" -oXo- ");
}

void draw_bullet(int x, int y)
{
	setcolor(4, 0);
	gotoxy(x, y);
	printf("|");
}

void draw_star(int x, int y)
{
	setcolor(4, 0);
	gotoxy(x, y);
	printf("*");
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
	printf(" ");
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

char cursor(int x, int y) 
{
	HANDLE hStd = GetStdHandle(STD_OUTPUT_HANDLE);
	char buf[2]; COORD c = { x,y }; DWORD num_read;
	if (!ReadConsoleOutputCharacter(hStd, (LPTSTR)buf, 1, c, (LPDWORD)&num_read))
		return '\0';
	else
		return buf[0];
}

void score(int score, int x, int y)
{
	setcolor(2, 0);
	gotoxy(x, y);
	printf("%d", score);
}