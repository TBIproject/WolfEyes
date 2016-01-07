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
        private static extern void mouse_event(uint dwFlags, uint dx, uint dy, uint cButtons, uint dwExtraInfo);

        private const int MOUSEEVENTF_LEFTDOWN = 0x02;
        private const int MOUSEEVENTF_LEFTUP = 0x04;
        private const int MOUSEEVENTF_RIGHTDOWN = 0x08;
        private const int MOUSEEVENTF_RIGHTUP = 0x10;

        private static bool stopThreads = false;
        private static List<Task> tasks = new List<Task>();
        private static bool running = false;
        private static bool oldClickState = false;

        public static bool Running
        {
            get
            {
                return running;
            }
        }

        public static void SetCameraOutput(int index, Preset.DetectionMethodEnum method, PictureBox output, bool count = false)
        {
            tasks.Add(new Task(() => CameraUpdate(index, method, output, count)));
        }

        public static void ReadCamera(int index, Preset.DetectionMethodEnum method, bool count = false)
        {
            tasks.Add(new Task(() => CameraUpdate(index, method, null, count)));
        }

        public static void EnableMouseControl()
        {
            tasks.Add(new Task(MouseControl));
        }

        public static void SetSpaceInfoOutput(Control output1O, Control output1I, Control output1J, Control output2O, Control output2I, Control output2J)
        {
            tasks.Add(new Task(() => SpaceInfoUpdate(output1O, output1I, output1J, output2O, output2I, output2J)));
        }

        public static void SetMouseInfoOutput(Control outputMouse)
        {
            tasks.Add(new Task(() => MouseInfoUpdate(outputMouse)));
        }

        public static void SetFingerInfoOutput(Control output, int index)
        {
            tasks.Add(new Task(() => FingerInfoUpdate(output, index)));
        }

        private static void MouseInfoUpdate(Control outputMouse)
        {
            D2Point mousePos;

            while (!Engine.stopThreads)
            {
                mousePos = ApplicationData.selectedPreset.Devices[0] % ApplicationData.selectedPreset.Devices[1];

                if (mousePos != null)
                    outputMouse.Invoke(new MethodInvoker(() => outputMouse.Text = mousePos.ToString()));

                Thread.Sleep(10);
            }
        }

        private static void FingerInfoUpdate(Control output, int index)
        {
            while (!Engine.stopThreads)
            {
                output.Invoke(new MethodInvoker(() =>
                {
                    if (ApplicationData.selectedPreset.Devices[index].Finger != null)
                    {
                        output.Text = ApplicationData.selectedPreset.Devices[index].Finger.ToString();
                    }
                }));

                Thread.Sleep(10);
            }
        }

        private static void SpaceInfoUpdate(Control output1O, Control output1I, Control output1J, Control output2O, Control output2I, Control output2J)
        {
            while (!Engine.stopThreads)
            {
                output1O.Invoke(new MethodInvoker(() =>
                {
                    if (ApplicationData.selectedPreset.Devices[0].Space != null)
                    {
                        output1O.Text = ApplicationData.selectedPreset.Devices[0].Space.o.ToString();
                        output1I.Text = ApplicationData.selectedPreset.Devices[0].Space.i.ToString();
                        output1J.Text = ApplicationData.selectedPreset.Devices[0].Space.j.ToString();
                    }

                    if (ApplicationData.selectedPreset.Devices[1].Space != null)
                    {
                        output2O.Text = ApplicationData.selectedPreset.Devices[1].Space.o.ToString();
                        output2I.Text = ApplicationData.selectedPreset.Devices[1].Space.i.ToString();
                        output2J.Text = ApplicationData.selectedPreset.Devices[1].Space.j.ToString();
                    }
                }));

                Thread.Sleep(100);
            }
        }

        private static void MouseControl()
        {
            while (!stopThreads)
            {
                SmoothMove(ApplicationData.selectedPreset.Devices, ApplicationData.selectedPreset.MouseDivider);

                if (ApplicationData.selectedPreset.Devices[0].Clicking && oldClickState == false)
                {
                    oldClickState = true;
                    mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0);
                }
                else if (!ApplicationData.selectedPreset.Devices[0].Clicking && oldClickState == true)
                {
                    oldClickState = false;
                    mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0);
                }

                Thread.Sleep(ApplicationData.selectedPreset.MouseThreadRate);
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

        private static void CameraUpdate(int index, Preset.DetectionMethodEnum method, PictureBox output, bool count)
        {
            ApplicationData.selectedPreset.Devices[index].SetFOV(Math.PI / 180 * 92);

            while (!stopThreads && ApplicationData.selectedPreset.Devices[index].CaptureDevice != null)
            {
                ApplicationData.selectedPreset.Devices[index].Band = new D2Point(ApplicationData.selectedPreset.BandMin, ApplicationData.selectedPreset.BandMax);
                ApplicationData.selectedPreset.Devices[index].BlurSize = ApplicationData.selectedPreset.Blur;
                ApplicationData.selectedPreset.Devices[index].Exposure = ApplicationData.selectedPreset.Exposure;

                Image<Bgr, byte> frame = ApplicationData.selectedPreset.Devices[index].GetNextFrame();
                Image<Bgr, byte> hand = null;

                if (frame != null)
                {
                    switch(method)
                    {
                        case Preset.DetectionMethodEnum.ByColor:
                            hand = ApplicationData.selectedPreset.Devices[index].DetectByColor(frame,
                                (byte)ApplicationData.selectedPreset.HueLowMin,
                                (byte)ApplicationData.selectedPreset.HueLowMax,
                                (byte)ApplicationData.selectedPreset.HueHighMin,
                                ApplicationData.selectedPreset.Threshold,
                                ApplicationData.selectedPreset.Dilate);
                            break;

                        case Preset.DetectionMethodEnum.ByReference:
                            hand = ApplicationData.selectedPreset.Devices[index].DetectByRef(frame, (byte)ApplicationData.selectedPreset.ThresholdDiff);
                            break;

                        case Preset.DetectionMethodEnum.Hybrid:
                            hand = ApplicationData.selectedPreset.Devices[index].DetectHybrid(frame,
                                (byte)ApplicationData.selectedPreset.HueLowMin,
                                (byte)ApplicationData.selectedPreset.HueLowMax,
                                (byte)ApplicationData.selectedPreset.HueHighMin,
                                (byte)ApplicationData.selectedPreset.Threshold,
                                (byte)ApplicationData.selectedPreset.ThresholdDiff,
                                ApplicationData.selectedPreset.Dilate,
                                ApplicationData.selectedPreset.MinSize);
                            break;

                        case Preset.DetectionMethodEnum.None:
                            output.Invoke(new MethodInvoker(() =>
                            {
                                output.BackgroundImage = frame.Bitmap;
                            }));
                            break;
                    }

                    if (hand != null)
                    {
                        //Image<Bgr, byte> scan = ApplicationData.selectedPreset.Devices[index].Skywalker(hand, ApplicationData.selectedPreset.Offshore, ApplicationData.selectedPreset.MinSize);

                        if (output != null)
                        {
                            output.Invoke(new MethodInvoker(() =>
                            {
                                //output.BackgroundImage = scan.Bitmap;
                                output.BackgroundImage = hand.Bitmap;
                            }));
                        }
                    }
                }

                Thread.Sleep(ApplicationData.selectedPreset.RefreshThreadRate);

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
