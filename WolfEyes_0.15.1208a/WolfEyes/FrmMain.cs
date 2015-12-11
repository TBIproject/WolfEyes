using Gma.System.MouseKeyHook;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace WolfEyes
{
    public partial class FrmMain : Form
    {
        private bool capturing = false;
        IKeyboardMouseEvents hook;
        bool down = false;

        [DllImport("user32.dll", CharSet = CharSet.Auto, CallingConvention = CallingConvention.StdCall)]
        public static extern void mouse_event(uint dwFlags, uint dx, uint dy, uint cButtons, uint dwExtraInfo);

        private const int MOUSEEVENTF_LEFTDOWN = 0x02;
        private const int MOUSEEVENTF_LEFTUP = 0x04;
        private const int MOUSEEVENTF_RIGHTDOWN = 0x08;
        private const int MOUSEEVENTF_RIGHTUP = 0x10;

        public FrmMain()
        {
            InitializeComponent();
            hook = Hook.GlobalEvents();
            hook.KeyDown += Hook_KeyDown;
            hook.KeyUp += hook_KeyUp;
        }

        void hook_KeyUp(object sender, KeyEventArgs e)
        {
            if (e.KeyCode == Keys.Insert)
            {
                if (down)
                {
                    down = false;
                    mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0);
                }
            }
        }

        private void Hook_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.KeyCode == Keys.F2)
            {
                ToggleEngine();
            }

            if(e.KeyCode == Keys.Insert)
            {
                if (!down)
                {
                    down = true;
                    mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0);
                }
            }
        }

        private void btnWizard_Click(object sender, EventArgs e)
        {
            ApplicationData.wizardStep = ApplicationData.WizardStep.SelectCamera;
            ApplicationData.WizardStep previous = ApplicationData.WizardStep.None;

            while (ApplicationData.wizardStep != previous)
            {
                previous = ApplicationData.wizardStep;

                switch (ApplicationData.wizardStep)
                {
                    case ApplicationData.WizardStep.SelectCamera:
                        new FrmSelectCamera().ShowDialog();
                        break;

                    case ApplicationData.WizardStep.SelectMode:
                        new FrmMode().ShowDialog();
                        break;

                    case ApplicationData.WizardStep.CameraSettings:
                        new FrmCameraSettings().ShowDialog();
                        break;

                    case ApplicationData.WizardStep.Calibration:
                        new FrmWizard().ShowDialog();
                        break;
                }
            }
        }

        private void UpdateEngine()
        {
            Engine.EnableMouseControl();
            Engine.ReadCamera(0, ApplicationData.detectionMethod, true);
            Engine.ReadCamera(1, ApplicationData.detectionMethod);
            Engine.StartEngine();
        }

        private void startCaptureToolStripMenuItem_Click(object sender, EventArgs e)
        {
            ToggleEngine();
        }

        private void ToggleEngine()
        {
            if (!capturing)
            {
                UpdateEngine();
                startCaptureToolStripMenuItem.Text = "Stop whiteboard engine";
            }
            else
            {
                Enabled = false;

                if (Engine.running)
                {
                    Enabled = true;

                    Engine.StopEngine(() =>
                    {
                        Invoke(new MethodInvoker(() => startCaptureToolStripMenuItem.Text = "Start whiteboard engine"));
                    });
                }
            }

            capturing = !capturing;
        }

        private void FrmMain_Load(object sender, EventArgs e)
        {
            //ApplicationData.cameras.Add(new Camera(0));
            //ApplicationData.cameras.Add(new Camera(1));
        }

        private void btnAdvanced1_Click(object sender, EventArgs e)
        {

        }

        private void FrmMain_FormClosing(object sender, FormClosingEventArgs e)
        {
            if (Engine.running)
            {
                e.Cancel = true;

                Engine.StopEngine(() =>
                {
                    Invoke(new MethodInvoker(() => Close()));
                });
            }
        }
    }
}
