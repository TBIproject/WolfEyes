using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace WolfEyes
{
    public partial class FrmSelectCamera : Form
    {
        public FrmSelectCamera()
        {
            InitializeComponent();
        }

        private void button2_Click(object sender, EventArgs e)
        {
            Close();
        }

        private void FrmSelectCamera_Load(object sender, EventArgs e)
        {
            UpdateEngine();
        }

        private void btnUpdate_Click(object sender, EventArgs e)
        {
            Enabled = false;
            Engine.StopEngine(() =>
            {
                UpdateEngine();
                Invoke(new MethodInvoker(() => Enabled = true));
            });
        }

        private void UpdateEngine()
        {
            ApplicationData.DeleteAllDevices();
            ApplicationData.RegisterDevice((int)nudDevice1.Value);
            ApplicationData.RegisterDevice((int)nudDevice2.Value);
            Engine.SetCameraOutput(0, Camera.DetectionMethod.None, picDevice1, true);
            Engine.SetCameraOutput(1, Camera.DetectionMethod.None, picDevice2);
            Engine.StartEngine();
        }

        private void FrmSelectCamera_FormClosing(object sender, FormClosingEventArgs e)
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

        private void btnNext_Click(object sender, EventArgs e)
        {
            ApplicationData.wizardStep = ApplicationData.WizardStep.SelectMode;
            Close();
        }
    }
}
