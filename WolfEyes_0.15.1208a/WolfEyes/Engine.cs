using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using Emgu.CV;
using Emgu.CV.Structure;
using Emgu.Util;
using System.Threading;
using System.Drawing;
using System.Runtime.InteropServices;

namespace WolfEyes
{
    class Engine
    {
        [DllImport("user32.dll", CharSet = CharSet.Auto, CallingConvention = CallingConvention.StdCall)]
        public static extern void mouse_event(uint dwFlags, uint dx, uint dy, uint cButtons, uint dwExtraInfo);

        private const int MOUSEEVENTF_LEFTDOWN = 0x02;
        private const int MOUSEEVENTF_LEFTUP = 0x04;
        private const int MOUSEEVENTF_RIGHTDOWN = 0x08;
        private const int MOUSEEVENTF_RIGHTUP = 0x10;

        public static bool stopThreads = false;
        public static List<Task> tasks = new List<Task>();
        public static bool running = false;
        private static bool oldClickState = false;

        public static void SetCameraOutput(int index, Camera.DetectionMethod method, PictureBox output, bool count = false)
        {
            tasks.Add(new Task(() => RefreshCamera(index, method, output, count)));
        }

        public static void ReadCamera(int index, Camera.DetectionMethod method, bool count = false)
        {
            tasks.Add(new Task(() => RefreshCamera(index, method, null, count)));
        }

        public static void EnableMouseControl()
        {
            tasks.Add(new Task(MouseControl));
        }

        private static void MouseControl()
        {
            while (!stopThreads)
            {
                SmoothMove(ApplicationData.devices, ApplicationData.mouseDivider);

                /*if (ApplicationData.devices[0].Clicking && oldClickState == false)
                {
                    oldClickState = true;
                    mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0);
                }
                else if (!ApplicationData.devices[0].Clicking && oldClickState == true)
                {
                    oldClickState = false;
                    mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0);
                }*/

                Thread.Sleep(ApplicationData.mouseThreadRate);
            }
        }

        private static void SmoothMove(List<Camera> devices, int divider)
        {
            D2Point finger = devices[0] % devices[1];
            if (finger != null)
            {
                D2Point diff = finger * new D2Point(Screen.PrimaryScreen.Bounds.Width, Screen.PrimaryScreen.Bounds.Height) - new D2Point(Cursor.Position.X, Cursor.Position.Y);
                D2Point v = diff.Unit() * diff.Length / divider;
                Cursor.Position = new Point(Cursor.Position.X + (int)v.x, Cursor.Position.Y + (int)v.y);
            }
        }

        private static void RefreshCamera(int index, Camera.DetectionMethod method, PictureBox output, bool count)
        {
            ApplicationData.devices[index].SetFOV(Math.PI / 180 * 92);

            while (!stopThreads && ApplicationData.devices[index].CaptureDevice != null)
            {
                ApplicationData.devices[index].Band = new D2Point(ApplicationData.bandMin, ApplicationData.bandMax);
                ApplicationData.devices[index].BlurSize = ApplicationData.blur;
                ApplicationData.devices[index].Exposure = ApplicationData.exposure;

                Image<Bgr, byte> frame = ApplicationData.devices[index].GetNextFrame();
                Image<Bgr, byte> hand = null;

                if (frame != null)
                {
                    switch(method)
                    {
                        case Camera.DetectionMethod.ByColor:
                            hand = ApplicationData.devices[index].DetectByColor(frame, (byte)ApplicationData.hueLowMin, (byte)ApplicationData.hueLowMax, (byte)ApplicationData.hueHighMin, ApplicationData.threshold, ApplicationData.dilate);
                            break;

                        case Camera.DetectionMethod.ByReference:
                            hand = ApplicationData.devices[index].DetectByRef(frame, (byte)ApplicationData.thresholdDiff);
                            break;

                        case Camera.DetectionMethod.Hybrid:
                            hand = ApplicationData.devices[index].DetectHybrid(frame, (byte)ApplicationData.hueLowMin, (byte)ApplicationData.hueLowMax, (byte)ApplicationData.hueHighMin, (byte)ApplicationData.threshold, (byte)ApplicationData.thresholdDiff, ApplicationData.dilate);
                            break;

                        case Camera.DetectionMethod.None:
                            output.Invoke(new MethodInvoker(() =>
                            {
                                output.BackgroundImage = frame.Bitmap;
                            }));
                            break;
                    }

                    if (hand != null)
                    {
                        Image<Bgr, byte> scan = ApplicationData.devices[index].Skywalker(hand, ApplicationData.offshore, ApplicationData.minSize);

                        if (output != null)
                        {
                            output.Invoke(new MethodInvoker(() =>
                            {
                                output.BackgroundImage = scan.Bitmap;
                            }));
                        }
                    }  
                }

                Thread.Sleep(ApplicationData.refreshThreadRate);

                if (count) ApplicationData.fpsCount++;
            }
        }

        public static void StartEngine()
        {
            stopThreads = false;
            running = true;
            foreach (Task task in tasks) task.Start();
        }

        public static void ClearThreads()
        {
            tasks = new List<Task>();
        }

        public static void StopEngine(Action callback = null, bool clearEngine = true)
        {
            if (callback != null)
                new Task(() => StopThreads(callback, clearEngine)).Start();
            else
                new Task(() => StopThreads(null, clearEngine)).Start();
        }

        private static void StopThreads(Action callback, bool clearEngine)
        {
            stopThreads = true;

            foreach (Task task in tasks)
                if (task != null)
                    task.Wait();

            if (clearEngine)
                ClearThreads();

            running = false;

            if (callback != null)
                callback();
        }
    }
}
