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
    public partial class FrmCalibration : Form
    {
        IKeyboardMouseEvents hook;
        DateTime start = DateTime.Now;

        public FrmCalibration(bool editing)
        {
            InitializeComponent();

            if(editing)
            {
                btnDone.Text = "Apply";
                btnDone.Enabled = false;
                btnPrevious.Enabled = false;
            }

            Size = new Size(Screen.PrimaryScreen.Bounds.Width, Screen.PrimaryScreen.Bounds.Height);
            hook = Hook.GlobalEvents();
            hook.KeyDown += Hook_KeyDown;
        }

        private void Hook_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.KeyCode == Keys.F1)
            {
                foreach (Camera device in ApplicationData.selectedPreset.Devices)
                    new Task(() => device.CumulativeReference(10)).Start();
            }

            if (e.KeyCode == Keys.F5)
            {
                lblInfo.Text = "Not calibrated";
                foreach (Camera device in ApplicationData.selectedPreset.Devices)
                    device.DefineSpaceWithFinger(Space.SpacePoint.O);
            }

            if (e.KeyCode == Keys.F6)
            {
                lblInfo.Text = "Not calibrated";
                foreach (Camera device in ApplicationData.selectedPreset.Devices)
                    device.DefineSpaceWithFinger(Space.SpacePoint.I);
            }

            if (e.KeyCode == Keys.F7)
            {
                lblInfo.Text = "Not calibrated";
                foreach (Camera device in ApplicationData.selectedPreset.Devices)
                    device.DefineSpaceWithFinger(Space.SpacePoint.J);
            }

            if (e.KeyCode == Keys.F9)
            {
                foreach (Camera device in ApplicationData.selectedPreset.Devices)
                    device.Calibrate();

                lblInfo.Text = "Calibrated !";
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
            Engine.SetSpaceInfoOutput(lblO, lblI, lblJ, lblO2, lblI2, lblJ2);
            Engine.SetMouseInfoOutput(lblMousePos);
            Engine.SetCameraOutput(0, ApplicationData.selectedPreset.DetectionMethod, picDevice1, true);
            Engine.SetCameraOutput(1, ApplicationData.selectedPreset.DetectionMethod, picDevice2);
            Engine.StartEngine();
        }

        private void btnDone_Click(object sender, EventArgs e)
        {
            Close();
        }

        private void FrmWizard_FormClosing(object sender, FormClosingEventArgs e)
        {
            if(ApplicationData.wizard.WizardStep == Wizard.WizardStepEnum.Calibration)
            {
                if (ApplicationData.selectedPreset.Devices[0].Space.IsDefined() && ApplicationData.selectedPreset.Devices[1].Space.IsDefined())
                {
                    e.Cancel = true;
                    MessageBox.Show("Spaces have not been defined !", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
                else
                {
                    if (Engine.Running)
                    {
                        foreach (Camera device in ApplicationData.selectedPreset.Devices)
                            device.Calibrate();

                        e.Cancel = true;

                        Engine.StopEngine(() =>
                        {
                            Invoke(new MethodInvoker(() => Close()));
                        });
                    }
                }
            }
            else
            {
                if (Engine.Running)
                {
                    e.Cancel = true;

                    Engine.StopEngine(() =>
                    {
                        Invoke(new MethodInvoker(() => Close()));
                    });
                }
            }
        }

        private void btnPrevious_Click(object sender, EventArgs e)
        {
            ApplicationData.wizard.SetNextStep(Wizard.WizardStepEnum.CameraSettings);

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

        private void panel1_Paint(object sender, PaintEventArgs e)
        {

        }
    }
}
