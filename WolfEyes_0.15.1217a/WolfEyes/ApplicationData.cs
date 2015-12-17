using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;
using Newtonsoft.Json;
using Newtonsoft.Json.Converters;
using System.Windows.Forms;

namespace WolfEyes
{
    class ApplicationData
    {
        public static Wizard wizard;
        public static Dictionary<string, Preset> presets = new Dictionary<string, Preset>();
        public static Preset selectedPreset = null;
        public static string workingDir = "";
        public static int fpsCount = 0;

        public static void LoadPreset(string fileName)
        {
            if (File.Exists(fileName))
            {
                string fileContent = File.ReadAllText(fileName);
                selectedPreset = (Preset)JsonConvert.DeserializeObject(fileContent, typeof(Preset), new StringEnumConverter());
                selectedPreset.FileName = fileName;
            }
            else
            {
                MessageBox.Show("The selected preset does not exist !", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        public static void SavePreset(string fileName)
        {
            string fileContent = JsonConvert.SerializeObject(presets[selectedPreset.Name]);
            File.WriteAllText(fileName, fileContent);
            selectedPreset.FileName = fileName;
        }
    }
}
