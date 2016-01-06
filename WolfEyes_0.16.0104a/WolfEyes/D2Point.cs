using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Drawing;

namespace WolfEyes
{
    public class D2Point
    {
        public double x;
        public double y;

        public D2Point(double x, double y)
        {
            this.x = x;
            this.y = y;
        }

        public static D2Point operator +(D2Point a, D2Point b)
        {
            return new D2Point(a.x + b.x, a.y + b.y);
        }

        public static D2Point operator -(D2Point a, D2Point b)
        {
            return new D2Point(a.x - b.x, a.y - b.y);
        }

        public static D2Point operator -(D2Point a, double b)
        {
            return a - new D2Point(b, b);
        }

        public static D2Point operator /(D2Point a, D2Point b)
        {
            return new D2Point(a.x / b.x, a.y / b.y);
        }

        public static D2Point operator /(D2Point a, double size)
        {
            return a / (new D2Point(size, size));
        }

        public static D2Point operator *(D2Point a, D2Point b)
        {
            return new D2Point(a.x * b.x, a.y * b.y);
        }

        public static D2Point operator *(D2Point a, double size)
        {
            return a * (new D2Point(size, size));
        }

        public static D2Point operator %(D2Point a, D2Point b)
        {
            return new D2Point((a.x + b.x) / 2, (a.y + b.y) / 2);
        }

        public static double Abs(D2Point a)
        {
            return Math.Sqrt(a.x * a.x + a.y * a.y);
        }

        public double Length
        {
            get
            {
                return Math.Sqrt(this.x * this.x + this.y * this.y);
            }
        }

        public D2Point Unit()
        {
            return this / this.Length;
        }

        public override string ToString()
        {
            return "X : " + x + " | Y : " + y;
        }
    }
}
