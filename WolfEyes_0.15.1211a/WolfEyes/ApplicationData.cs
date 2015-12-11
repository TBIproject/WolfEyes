using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace WolfEyes
{
    class ApplicationData
    {
        public static Wizard wizard;
        public static Dictionary<string, Preset> presets = new Dictionary<string, Preset>();
        public static Preset selectedPreset = null;
        public static int fpsCount = 0;

        public static void LoadPresetsFrom(string location)
        {

        }
    }
}
