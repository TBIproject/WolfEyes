using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace WolfEyes
{
    public class Space
    {
        public double o;
        public double i;
        public double j;

        public enum SpacePoint
        {
            O,
            I,
            J
        }

        public Space()
        {
            o = 0;
            i = 0;
            j = 0;
        }

        public bool IsDefined()
        {
            return o != 0 && i != 0 && j != 0;
        }

        public override string ToString()
        {
            return "O : " + o + " I : " + i + " J : " + j;
        }
    }
}
