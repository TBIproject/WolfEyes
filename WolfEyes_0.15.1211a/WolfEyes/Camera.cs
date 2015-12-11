using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Emgu.CV;
using Emgu.CV.CvEnum;
using Emgu.CV.Structure;
using System.Drawing;
using System.Windows.Forms;
using Emgu.CV.Util;
using Emgu.CV.VideoSurveillance;
using System.Threading;

namespace WolfEyes
{
    public class Camera
    {
        private Capture captureDevice;
        private D2Point fingerPosition;
        private Space virtualSpace = new Space();
        private D2Point fov = new D2Point(0, 0);
        private D2Point band = new D2Point(0, 1);
        private int resolution = 1;
        private D2Point cameraPosition = new D2Point(0,0);
        private Image<Bgr, byte> referenceFrame;
        private int blurSize = 0;
        private bool clicking = false;

        public Space Space
        {
            get
            {
                return virtualSpace;
            }
        }

        public bool Clicking
        {
            get
            {
                return clicking;
            }
        }

        public D2Point Band
        {
            get
            {
                return band;
            }
            set
            {
                band = value;
            }
        }

        public D2Point FOV
        {
            get
            {
                return fov;
            }
            set
            {
                fov = value;
            }
        }

        public double Exposure {
            get
            {
                return GetProp(CapProp.Exposure);
            }
            set
            {
                SetProp(CapProp.Exposure, value);
            }
        }

        public double Height
        {
            get
            {
                return GetProp(CapProp.FrameHeight);
            }
            set
            {
                SetProp(CapProp.FrameHeight, value);
            }
        }

        public double Width
        {
            get
            {
                return GetProp(CapProp.FrameWidth);
            }
            set
            {
                SetProp(CapProp.FrameWidth, value);
            }
        }

        public double FPS
        {
            get
            {
                return GetProp(CapProp.Fps);
            }
            set
            {
                SetProp(CapProp.Fps, value);
            }
        }

        public bool IsInit
        {
            get
            {
                return captureDevice != null;
            }
        }

        public int BlurSize
        {
            get
            {
                return blurSize;
            }
            set
            {
                blurSize = value;
            }
        }

        public Image<Bgr, byte> ReferenceFrame
        {
            get
            {
                return referenceFrame;
            }
        }

        public D2Point CameraPosition
        {
            get
            {
                return cameraPosition;
            }
        }

        public D2Point Finger
        {
            get
            {
                return fingerPosition;
            }
        }

        public Space VirtualSpace
        {
            get
            {
                return virtualSpace;
            }
        }

        public Capture CaptureDevice
        {
            get
            {
                return captureDevice;
            }
        }

        private int id;

        public int ID
        {
            get { return id; }
        }

        public void SetFOV(double horizontal=0, double vertical=0)
        {
            fov.x = horizontal;
            fov.y = vertical;
        }

        private double GetProp(CapProp prop)
        {
            return captureDevice.GetCaptureProperty(prop);
        }

        private void SetProp(CapProp prop, double value)
        {
            captureDevice.SetCaptureProperty(prop, value);
        }

        public Camera(int id)
        {
            try
            {
                captureDevice = new Capture(id);
                this.id = id;
                //captureDevice.QueryFrame();
                UpdateReference();
                //FPS = 9999.9; // Provoque le crash du programme
            }
            catch
            {
                MessageBox.Show("No compatible devices available !", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                //MessageBox.Show(e.Message, "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                captureDevice = null;
            }
        }

        public void SetImageVertBand(double a, double b, int r)
        {
            band = new D2Point(a, b);
            resolution = r;
        }

        public Image<Bgr, byte> GetNextFrame()
        {
            try
            {
                Image<Bgr, byte> frame = captureDevice.QueryFrame().ToImage<Bgr, byte>();

                if (frame != null)
                {
                    int a = (int)(band.x * Height);
                    int b = (int)(band.y * Height);
                    frame.ROI = new Rectangle(0, a, frame.Width, b - a);
                    if (blurSize > 0) frame = frame.SmoothBlur(blurSize, blurSize);
                }

                return frame;
            }
            catch
            {
                return null;
            }
        }

        public void UpdateReference()
        {
            try
            {
                referenceFrame = captureDevice.QueryFrame().ToImage<Bgr, byte>();
            }
            catch
            {
                referenceFrame = null;
            }
        }

        public void CumulativeReference(int count)
        {
            try
            {
                Image<Bgr, int> cumulative = new Image<Bgr,int>((int)Width, (int)Height);
                Image<Bgr, int> frame = new Image<Bgr, int>((int)Width, (int)Height);
                Image<Bgr, byte> result = new Image<Bgr,byte>((int)Width, (int)Height);

                for (int i = 0; i < count; i++ )
                {
                    frame = captureDevice.QueryFrame().ToImage<Bgr, int>();
                    
                    // Différence entre result et frame

                    cumulative += frame;
                    Thread.Sleep(1000 / count);
                }

                result = (cumulative / count).Convert<Bgr, byte>();

                referenceFrame = result;
            }
            catch
            {
                referenceFrame = null;
            }
        }

        public void Release()
        {
            captureDevice.Dispose();
        }

        public void Calibrate()
        {
            double a = fov.x * (virtualSpace.i - virtualSpace.o);
            double b = fov.x * (virtualSpace.o - virtualSpace.j);
		
		    double Ca = 1 - 1.0/Math.Tan(a);
		    double Cb = 1 - 1.0/Math.Tan(b);
		    double k = Cb/Ca;

            cameraPosition.x = (1 + k / Math.Tan(a)) / (1 + k * k);
            cameraPosition.y = cameraPosition.x * k;
        }

        public double FingerAbsoluteAngle()
        {
            if (fingerPosition == null) return -1;

            double finger = fingerPosition.x * fov.x;
            double O = virtualSpace.o * fov.x;
            double offset = 0;

            if (cameraPosition.x != 0)
                offset = Math.Atan(cameraPosition.y / cameraPosition.x);
            else if (cameraPosition.y > 0)
                offset = Math.PI / 180 * 90.0;
            else if (cameraPosition.y < 0)
                offset = Math.PI / 180 * -90.0;

            return (Math.PI + offset) - (O - finger);
        }

        public D2Point FingerPosition(Camera camera)
        {
            if (fingerPosition == null || camera.fingerPosition == null || cameraPosition == null || camera.cameraPosition == null)
                return null;

            D2Point point = new D2Point(0, 0);
            double a = Math.Tan(FingerAbsoluteAngle());
            double b = cameraPosition.y - a * cameraPosition.x;

            double c = Math.Tan(camera.FingerAbsoluteAngle());
            double d = camera.cameraPosition.y - c * camera.cameraPosition.x;

            if (a != c)
            {
                point.x = (d - b) / (a - c);
                point.y = 1-(a * point.x + b);

                clicking = (fingerPosition.y > 0.85 && camera.fingerPosition.y > 0.85);

                return point;
            }
            else
            {
                clicking = false;
                return null;
            }
        }

        public static D2Point operator %(Camera a, Camera b)
        {
            return a.FingerPosition(b);
        }

        public Image<Bgr, byte> Skywalker(Image<Bgr, byte> bin, int offshore, double minSize, bool blur=false)
        {
            Image<Bgr, byte> scan = bin.Copy();

            if (blur) scan.SmoothBlur(3, 3);

            int step = 0;
            D2Point start = null, end = null;
            D2Point size = new D2Point(scan.Width, scan.Height);
            D2Point ratio = (minSize < 1 ? size : new D2Point(1, 1));

            for (int y = (int)size.y - 1; y > -1; y--)
            {
                for (int x = 0; x < (int)size.x; x++)
                {
                    if(scan.Data[y,x,0] > 0)
                    {
                        scan.Data[y, x, 0] = 0;
                        scan.Data[y, x, 1] = 0;
                        scan.Data[y, x, 2] = 255;
                        step = 0;

                        if(start == null)
                        {
                            start = new D2Point(x, y);
                            end = new D2Point(x, y);
                        }
                        else
                        {
                            end.x = x;
                            end.y = y;
                        }
                    }
                    else if(end != null)
                    {
                        if (step < offshore)
                        {
                            scan.Data[y, x, 0] = 0;
                            scan.Data[y, x, 1] = 255;
                            scan.Data[y, x, 2] = 255;
                            step++;
                        }
                        else if (D2Point.Abs((start - end) / ratio) <= minSize)
                        {
                            start = null;
                            end = null;
                        }
                        else break;
                    }
                }
                if (end != null) break;
            }

            if (end != null)
            {
                D2Point result = start % end;

                for (int y = scan.Height; --y >= result.y;)
                {
                    scan.Data[y, (int)result.x, 0] = 0;
                    scan.Data[y, (int)result.x, 1] = 255;
                    scan.Data[y, (int)result.x, 2] = 0;
                }

                result /= size;
                result.x = 1 - result.x;
                fingerPosition = result;
            }

            return scan;
        }

        public void Saber()
        {
             
        }

        public Image<Bgr, byte> DetectByColor(Image<Bgr, byte> frame, byte hueLowMin, byte hueLowMax, byte hueHighMin, int threshold, int dilate)
        {
            Image<Hsv, byte> hsv = frame.Convert<Hsv, byte>();
            Image<Lab, byte> lab = frame.Convert<Lab, byte>();
            Image<Ycc, byte> ycrcb = frame.Convert<Ycc, byte>();

            Image<Gray, byte> h = hsv.Split()[0];
            Image<Gray, byte> a = lab.Split()[1];
            Image<Gray, byte> cr = ycrcb.Split()[1];

            for (int y = h.Rows; --y >= 0;)
            {
                for (int x = h.Cols; --x >= 0;)
                {
                    if((h.Data[y, x, 0] > hueLowMin && h.Data[y, x, 0] < hueLowMax) || h.Data[y, x, 0] > hueHighMin)
                        h.Data[y, x, 0] = 255;
                    else
                        h.Data[y, x, 0] = 0;
                }
            }

            a = Threshold(a, 130);
            cr = Threshold(cr, 145);

            Image<Gray, byte> result = (h/3 + a/3 + cr/3);
            result = result.Erode(dilate);
            result = result.Dilate(dilate);
            result = Threshold(result, threshold);

            return result.Convert<Bgr, byte>();
        }

        public Image<Bgr, byte> DetectHybrid(Image<Bgr, byte> frame, byte hueLowMin, byte hueLowMax, byte hueHighMin, int threshold, int diffThreshold, int dilate)
        {
            Image<Hsv, byte> hsv = frame.Convert<Hsv, byte>();
            Image<Lab, byte> lab = frame.Convert<Lab, byte>();
            Image<Ycc, byte> ycrcb = frame.Convert<Ycc, byte>();

            Image<Gray, byte> h = hsv.Split()[0];
            Image<Gray, byte> a = lab.Split()[1];
            Image<Gray, byte> cr = ycrcb.Split()[1];

            for (int y = h.Rows; --y >= 0; )
            {
                for (int x = h.Cols; --x >= 0; )
                {
                    if ((h.Data[y, x, 0] > hueLowMin && h.Data[y, x, 0] < hueLowMax) || h.Data[y, x, 0] > hueHighMin)
                        h.Data[y, x, 0] = 255;
                    else
                        h.Data[y, x, 0] = 0;
                }
            }

            a = Threshold(a, 130);
            cr = Threshold(cr, 145);

            int aa = (int)(band.x * Height);
            int bb = (int)(band.y * Height);
            referenceFrame.ROI = new Rectangle(0, aa, frame.Width, (bb - aa));

            Image<Bgr, byte> tempRef = referenceFrame.Copy();

            Image<Gray, byte> diff = frame.AbsDiff(tempRef).Convert<Gray, byte>();

            Image<Gray, byte> result = (h / 3 + a / 3 + diff / 3);
            result = result.Erode(dilate);
            result = result.Dilate(dilate);
            result = Threshold(result, threshold);

            return result.Convert<Bgr, byte>();
        }

        public Image<Bgr, byte> DetectByRef(Image<Bgr, byte> frame, int diffThreshold)
        {
            try
            {
                int a = (int)(band.x * Height);
                int b = (int)(band.y * Height);
                referenceFrame.ROI = new Rectangle(0, a, frame.Width, (b - a));

                Image<Bgr, byte> tempRef = referenceFrame.Copy();

                Image<Gray, byte> diff = frame.AbsDiff(tempRef).Convert<Gray, byte>();

                diff = Threshold(diff, diffThreshold);

                return diff.Convert<Bgr, byte>();
            }
            catch
            {
                return null;
            }
        }

        public Image<Bgr, byte> DetectTest(Image<Bgr, byte> frame)
        {
            Image<Hsv, byte> hsv = frame.Convert<Hsv, byte>();

            VectorOfMat test = new VectorOfMat();
            

            for(int y = hsv.Rows; --y >= 0;)
            {
                for (int x = hsv.Cols; --x >= 0; )
                {
                    hsv.Data[y, x, 0] = (byte)(hsv.Data[y, x, 0] / 15 * 15);
                    hsv.Data[y, x, 1] = 255;
                    hsv.Data[y, x, 2] = 255;
                }
            }

            return hsv.Convert<Bgr, byte>();
        }


        public Image<Gray, byte> Threshold(Image<Gray, byte> frame, int threshold)
        {
            /*for (int y = frame.Rows; --y >= 0;)
            {
                for (int x = frame.Cols; --x >= 0;)
                {
                    frame.Data[y, x, 0] = (byte)((frame.Data[y, x, 0] > threshold) ? 255 : 0);
                }
            }*/

           return frame.InRange(new Gray(threshold), new Gray(255));
        }
    }
}
