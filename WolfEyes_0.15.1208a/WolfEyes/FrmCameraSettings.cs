using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using Gma.System.MouseKeyHook;

namespace WolfEyes
{
    public partial class FrmCameraSettings : Form
    {
        IKeyboardMouseEvents hook;

        public FrmCameraSettings()
        {
            InitializeComponent();
            hook = Hook.GlobalEvents();
            hook.KeyDown += Hook_KeyDown;
        }

        private void FrmCameraSettings_Load(object sender, EventArgs e)
        {
            //nudBandBottom.Value = Convert.ToInt32(ApplicationData.bandMin * 100);
            //nudBandTop.Value = Convert.ToInt32(ApplicationData.bandMax * 100);
            nudBlur.Value = ApplicationData.blur;
            nudByColorDilate.Value = ApplicationData.dilate;
            nudByColorThresh.Value = ApplicationData.threshold;
            nudByRefThresh.Value = ApplicationData.thresholdDiff;
            nudExposure.Value = ApplicationData.exposure;
            nudHueHighMin.Value = ApplicationData.hueHighMin;
            nudHueLowMax.Value = ApplicationData.hueLowMax;
            nudHueLowMin.Value = ApplicationData.hueLowMin;
            nudMinSize.Value = ApplicationData.minSize;
            nudOffshore.Value = ApplicationData.offshore;

            lblBandBottom.Text = ApplicationData.bandMin.ToString();
            lblBandTop.Text = ApplicationData.bandMax.ToString();
            lblBlur.Text = ApplicationData.blur.ToString();
            lblByColorDilate.Text = ApplicationData.dilate.ToString();
            lblByColorThresh.Text = ApplicationData.threshold.ToString();
            lblByRefThresh.Text = ApplicationData.thresholdDiff.ToString();
            lblExposure.Text = ApplicationData.exposure.ToString();
            lblHueHighMin.Text = ApplicationData.hueHighMin.ToString();
            lblHueLowMax.Text = ApplicationData.hueLowMax.ToString();
            lblHueLowMin.Text = ApplicationData.hueLowMin.ToString();
            lblMinSize.Text = ApplicationData.minSize.ToString();
            lblOffshore.Text = ApplicationData.offshore.ToString();

            UpdateEngine();
        }

        private void Hook_KeyDown(object sender, KeyEventArgs e)
        {
            if(e.KeyCode == Keys.F1)
            { 
                foreach (Camera device in ApplicationData.devices)
                    new Task(() => device.CumulativeReference(10)).Start();
            }
        }

        private void UpdateEngine()
        {
            Engine.SetCameraOutput(0, ApplicationData.detectionMethod, picDevice1, true);
            Engine.SetCameraOutput(1, ApplicationData.detectionMethod, picDevice2);
            Engine.StartEngine();
        }

        private void btnCancel_Click(object sender, EventArgs e)
        {
            Close();
        }

        private void btnNext_Click(object sender, EventArgs e)
        {
            ApplicationData.wizardStep = ApplicationData.WizardStep.Calibration;
            Close();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            ApplicationData.wizardStep = ApplicationData.WizardStep.SelectMode;
            Close();
        }

        private void nudHueLowMin_Scroll(object sender, EventArgs e)
        {
            lblHueLowMin.Text = nudHueLowMin.Value.ToString();
            ApplicationData.hueLowMin = nudHueLowMin.Value;
        }

        private void nudHueLowMax_Scroll(object sender, EventArgs e)
        {
            lblHueLowMax.Text = nudHueLowMax.Value.ToString();
            ApplicationData.hueLowMax = nudHueLowMax.Value;
        }

        private void nudHueHighMin_Scroll(object sender, EventArgs e)
        {
            lblHueHighMin.Text = nudHueHighMin.Value.ToString();
            ApplicationData.hueHighMin = nudHueHighMin.Value;
        }

        private void nudBlur_Scroll(object sender, EventArgs e)
        {
            lblBlur.Text = nudBlur.Value.ToString();
            ApplicationData.blur = nudBlur.Value;
        }

        private void nudExposure_Scroll(object sender, EventArgs e)
        {
            lblExposure.Text = nudExposure.Value.ToString();
            ApplicationData.exposure = nudExposure.Value;
        }

        private void nudMinSize_Scroll(object sender, EventArgs e)
        {
            lblMinSize.Text = nudMinSize.Value.ToString();
            ApplicationData.minSize = nudMinSize.Value;
        }

        private void nudOffshore_Scroll(object sender, EventArgs e)
        {
            lblOffshore.Text = nudOffshore.Value.ToString();
            ApplicationData.offshore = nudOffshore.Value;
        }

        private void nudByColorThresh_Scroll(object sender, EventArgs e)
        {
            lblByColorThresh.Text = nudByColorThresh.Value.ToString();
            ApplicationData.threshold = nudByColorThresh.Value;
        }

        private void nudByRefThresh_Scroll(object sender, EventArgs e)
        {
            lblByRefThresh.Text = nudByRefThresh.Value.ToString();
            ApplicationData.thresholdDiff = nudByRefThresh.Value;
        }

        private void nudByColorDilate_Scroll(object sender, EventArgs e)
        {
            lblByColorDilate.Text = nudByColorDilate.Value.ToString();
            ApplicationData.dilate = nudByColorDilate.Value;
        }

        private void nudBandTop_Scroll(object sender, EventArgs e)
        {
            lblBandTop.Text = (nudBandTop.Value / 100.0).ToString();
            ApplicationData.bandMin = nudBandTop.Value / 100.0;
        }

        private void nudBandBottom_Scroll(object sender, EventArgs e)
        {
            lblBandBottom.Text = (nudBandBottom.Value / 100.0).ToString();
            ApplicationData.bandMax = nudBandBottom.Value / 100.0;
        }

        private void FrmCameraSettings_FormClosing(object sender, FormClosingEventArgs e)
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
