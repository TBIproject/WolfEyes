using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace WolfEyes
{
    class ApplicationData
    {
        public enum WizardStep
        {
            SelectCamera,
            SelectMode,
            CameraSettings,
            Calibration,
            None
        }

        public static WizardStep wizardStep;

        public static int refreshThreadRate = 1;
        public static int mouseThreadRate = 10;

        public static int hueLowMin = 0;
        public static int hueLowMax = 21;
        public static int hueHighMin = 170;
        public static double bandMin = 0;
        public static double bandMax = 1;
        public static int blur = 6;
        public static int minSize = 3;
        public static int offshore = 5;
        public static int exposure = -5;
        public static int threshold = 100;
        public static int thresholdDiff = 50;
        public static int dilate = 10;
        public static int simplifier = 1;

        public static Camera.DetectionMethod detectionMethod = Camera.DetectionMethod.None;

        public static List<Camera> devices = new List<Camera>();

        public static int mouseDivider = 10;
        public static int fpsCount = 0;

        public static void RegisterDevice(int id)
        {
            devices.Add(new Camera(id));
        }

        public static void DeleteAllDevices()
        {
            foreach (Camera device in devices)
                device.CaptureDevice.Dispose();
            devices = new List<Camera>();
        }
    }
}
