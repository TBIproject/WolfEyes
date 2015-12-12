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
    public partial class FrmPresetName : Form
    {
        public FrmPresetName(bool editing)
        {
            InitializeComponent();
            if (editing)
            {
                btnCancel.Text = "Apply";
                btnNext.Enabled = false;
            }
        }

        private void button1_Click(object sender, EventArgs e)
        {
            if (!ApplicationData.presets.ContainsKey(textBox1.Text))
            {
                ApplicationData.selectedPreset.Name = textBox1.Text;
                ApplicationData.wizard.SetNextStep(Wizard.WizardStepEnum.SelectCamera);
                Close();
            }
            else
            {
                MessageBox.Show("This preset name is already used.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void button2_Click(object sender, EventArgs e)
        {
            Close();
        }

        private void FrmPresetName_Load(object sender, EventArgs e)
        {
            textBox1.Text = ApplicationData.selectedPreset.Name;
        }

        private void panel1_Paint(object sender, PaintEventArgs e)
        {

        }
    }
}
