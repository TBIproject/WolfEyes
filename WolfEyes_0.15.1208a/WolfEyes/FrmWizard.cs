using Gma.System.MouseKeyHook;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace WolfEyes
{
    public partial class FrmWizard : Form
    {
        IKeyboardMouseEvents hook;
        DateTime start = DateTime.Now;

        public FrmWizard()
        {
            InitializeComponent();
            Size = new Size(Screen.PrimaryScreen.Bounds.Width, Screen.PrimaryScreen.Bounds.Height);
            hook = Hook.GlobalEvents();
            hook.KeyDown += Hook_KeyDown;
        }

        private void Hook_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.KeyCode == Keys.F1)
            {
                foreach (Camera device in ApplicationData.devices)
                    new Task(() => device.CumulativeReference(10)).Start();
            }

            if (e.KeyCode == Keys.F5)
            {
                lblInfo.Text = "Not calibrated";
                foreach (Camera device in ApplicationData.devices)
                    device.Space.o = device.Finger.x;
            }

            if (e.KeyCode == Keys.F6)
            {
                lblInfo.Text = "Not calibrated";
                foreach (Camera device in ApplicationData.devices)
                    device.Space.i = device.Finger.x;
            }

            if (e.KeyCode == Keys.F7)
            {
                lblInfo.Text = "Not calibrated";
                foreach (Camera device in ApplicationData.devices)
                    device.Space.j = device.Finger.x;
            }

            if (e.KeyCode == Keys.F9)
            {
                foreach (Camera device in ApplicationData.devices)
                    device.Calibrate();

                lblInfo.Text = "Calibrated !";
            }
        }

        private void Debug()
        {
            D2Point mousePos;

            while (!Engine.stopThreads)
            {
                Invoke(new MethodInvoker(() =>
                {
                    if (ApplicationData.devices[0].Finger != null)
                    {
                        lblO.Text = ApplicationData.devices[0].Space.o.ToString();
                        lblI.Text = ApplicationData.devices[0].Space.i.ToString();
                        lblJ.Text = ApplicationData.devices[0].Space.j.ToString();
                    }

                    if (ApplicationData.devices[1].Finger != null)
                    {
                        lblO2.Text = ApplicationData.devices[1].Space.o.ToString();
                        lblI2.Text = ApplicationData.devices[1].Space.i.ToString();
                        lblJ2.Text = ApplicationData.devices[1].Space.j.ToString();
                    }

                    mousePos = ApplicationData.devices[0] % ApplicationData.devices[1];

                    if (mousePos != null)
                        lblMousePos.Text = mousePos.ToString();
                }));

                Thread.Sleep(10);
            }
        }

        private void frmWizard_Load(object sender, EventArgs e)
        {
            UpdateEngine();
            picPointJ.Location = new Point(0, 0);
            picPointO.Location = new Point(0, Height - picPointO.Height);
            picPointI.Location = new Point(Width - picPointI.Width, Height - picPointI.Height);
            picPointITemp.Location = new Point(Height - picPointI.Width / 2, Height - picPointITemp.Height);
        }

        private void UpdateEngine()
        {
            Engine.tasks.Add(new Task(Debug));
            Engine.SetCameraOutput(0, ApplicationData.detectionMethod, picDevice1, true);
            Engine.SetCameraOutput(1, ApplicationData.detectionMethod, picDevice2);
            Engine.StartEngine();
        }

        private void btnDone_Click(object sender, EventArgs e)
        {
            Close();
        }

        private void FrmWizard_FormClosing(object sender, FormClosingEventArgs e)
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

        private void btnPrevious_Click(object sender, EventArgs e)
        {
            ApplicationData.wizardStep = ApplicationData.WizardStep.CameraSettings;
            Close();
        }

        private void btnCancel_Click(object sender, EventArgs e)
        {
            Close();
        }

        private void numericUpDown1_ValueChanged(object sender, EventArgs e)
        {
            picPointJ.Location = new Point(0 + (int)nudOffset.Value, 0 + (int)nudOffset.Value);
            picPointO.Location = new Point(0 + (int)nudOffset.Value, Height - picPointO.Height - (int)nudOffset.Value);
            picPointI.Location = new Point(Width - picPointI.Width - (int)nudOffset.Value, Height - picPointI.Height - (int)nudOffset.Value);
            picPointITemp.Location = new Point(Height - picPointI.Width / 2 - (int)nudOffset.Value, Height - picPointITemp.Height - (int)nudOffset.Value);
        }
    }
}
