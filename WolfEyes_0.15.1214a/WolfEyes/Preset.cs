using Newtonsoft.Json;
using Newtonsoft.Json.Converters;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace WolfEyes
{
    class Preset
    {
        public enum DetectionMethodEnum
        {
            ByColor,
            ByReference,
            Hybrid,
            None
        }

        private string fileName = "";

        [JsonIgnore]
        public string FileName
        {
            get
            {
                return fileName;
            }
            set
            {
                fileName = value;
            }
        }

        private string name = "new preset";
        public string Name
        {
            get { return name; }
            set { name = value; }
        }

        private int refreshThreadRate = 1;
        public int RefreshThreadRate
        {
            get { return refreshThreadRate; }
            set { refreshThreadRate = value; }
        }

        private int mouseThreadRate = 10;
        public int MouseThreadRate
        {
            get { return mouseThreadRate; }
            set { mouseThreadRate = value; }
        }

        private int hueLowMin = 0;
        public int HueLowMin
        {
            get { return hueLowMin; }
            set { hueLowMin = value; }
        }

        private int hueLowMax = 21;
        public int HueLowMax
        {
            get { return hueLowMax; }
            set { hueLowMax = value; }
        }

        private int hueHighMin = 170;
        public int HueHighMin
        {
            get { return hueHighMin; }
            set { hueHighMin = value; }
        }

        private double bandMin = 0;
        public double BandMin
        {
            get { return bandMin; }
            set
            {
                if (value < bandMax)
                    bandMin = value;
            }
        }

        private double bandMax = 1;
        public double BandMax
        {
            get { return bandMax; }
            set
            {
                if (value > bandMin)
                    bandMax = value;
            }
        }

        private int blur = 6;
        public int Blur
        {
            get { return blur; }
            set { blur = value; }
        }

        private int minSize = 3;
        public int MinSize
        {
            get { return minSize; }
            set { minSize = value; }
        }

        private int offshore = 5;
        public int Offshore
        {
            get { return offshore; }
            set { offshore = value; }
        }

        private int exposure = -5;
        public int Exposure
        {
            get { return exposure; }
            set { exposure = value; }
        }

        private int threshold = 100;
        public int Threshold
        {
            get { return threshold; }
            set { threshold = value; }
        }

        private int thresholdDiff = 50;
        public int ThresholdDiff
        {
            get { return thresholdDiff; }
            set { thresholdDiff = value; }
        }

        private int dilate = 10;
        public int Dilate
        {
            get { return dilate; }
            set { dilate = value; }
        }

        private int simplifier = 1;
        public int Simplifier
        {
            get { return simplifier; }
            set { simplifier = value; }
        }

        private DetectionMethodEnum detectionMethod = DetectionMethodEnum.None;

        [JsonConverter(typeof(StringEnumConverter))]
        public DetectionMethodEnum DetectionMethod
        {
            get { return detectionMethod; }
            set { detectionMethod = value; }
        }

        private int mouseDivider = 10;
        public int MouseDivider
        {
            get { return mouseDivider; }
            set { mouseDivider = value; }
        }

        private List<Camera> devices = new List<Camera>();

        [JsonIgnore]
        public List<Camera> Devices
        {
            get { return devices; }
            set { devices = value; }
        }

        public int[] DevicesID
        {
            get
            {
                int[] temp = new int[devices.Count];
                int i = 0;

                foreach(Camera device in devices)
                    temp[i++] = device.ID;

                return temp;
            }

            set
            {
                devices = new List<Camera>();

                foreach(int id in value)
                    devices.Add(new Camera(id));
            }
        }

        public Preset()
        {

        }

        public void RegisterDevice(int id)
        {
            devices.Add(new Camera(id));
        }

        public void DeleteAllDevices()
        {
            foreach (Camera device in devices)
                device.CaptureDevice.Dispose();
            devices = new List<Camera>();
        }
    }
}
