namespace WolfEyes
{
    partial class FrmMain
    {
        /// <summary>
        /// Variable nécessaire au concepteur.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Nettoyage des ressources utilisées.
        /// </summary>
        /// <param name="disposing">true si les ressources managées doivent être supprimées ; sinon, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Code généré par le Concepteur Windows Form

        /// <summary>
        /// Méthode requise pour la prise en charge du concepteur - ne modifiez pas
        /// le contenu de cette méthode avec l'éditeur de code.
        /// </summary>
        private void InitializeComponent()
        {
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(FrmMain));
            this.tabControl1 = new System.Windows.Forms.TabControl();
            this.tabPage1 = new System.Windows.Forms.TabPage();
            this.cbxPresets = new System.Windows.Forms.ComboBox();
            this.label2 = new System.Windows.Forms.Label();
            this.label1 = new System.Windows.Forms.Label();
            this.button3 = new System.Windows.Forms.Button();
            this.button2 = new System.Windows.Forms.Button();
            this.button1 = new System.Windows.Forms.Button();
            this.btnWizard = new System.Windows.Forms.Button();
            this.tabPage2 = new System.Windows.Forms.TabPage();
            this.lblPresetWarning = new System.Windows.Forms.Label();
            this.btnCalibrate = new System.Windows.Forms.Button();
            this.btnDeviceSettings = new System.Windows.Forms.Button();
            this.btnAlgorithmSelection = new System.Windows.Forms.Button();
            this.btnPresetName = new System.Windows.Forms.Button();
            this.btnDeviceSelection = new System.Windows.Forms.Button();
            this.menuStrip1 = new System.Windows.Forms.MenuStrip();
            this.fileToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.loadPresetToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.savePresetToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.savePresetToolStripMenuItem1 = new System.Windows.Forms.ToolStripMenuItem();
            this.savePresetAsToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.toolStripSeparator1 = new System.Windows.Forms.ToolStripSeparator();
            this.quitToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.settingsToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.performanceSettingsToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.startCaptureToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.aboutToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.helpToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.aboutWolfEyesToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.panel1 = new System.Windows.Forms.Panel();
            this.lblEngine = new System.Windows.Forms.Label();
            this.lblLoadedPreset = new System.Windows.Forms.Label();
            this.label4 = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.saveFileDialog1 = new System.Windows.Forms.SaveFileDialog();
            this.openFileDialog1 = new System.Windows.Forms.OpenFileDialog();
            this.tabControl1.SuspendLayout();
            this.tabPage1.SuspendLayout();
            this.tabPage2.SuspendLayout();
            this.menuStrip1.SuspendLayout();
            this.panel1.SuspendLayout();
            this.SuspendLayout();
            // 
            // tabControl1
            // 
            this.tabControl1.Controls.Add(this.tabPage1);
            this.tabControl1.Controls.Add(this.tabPage2);
            this.tabControl1.Dock = System.Windows.Forms.DockStyle.Fill;
            this.tabControl1.Location = new System.Drawing.Point(0, 24);
            this.tabControl1.Name = "tabControl1";
            this.tabControl1.SelectedIndex = 0;
            this.tabControl1.Size = new System.Drawing.Size(514, 376);
            this.tabControl1.TabIndex = 0;
            this.tabControl1.Selecting += new System.Windows.Forms.TabControlCancelEventHandler(this.tabControl1_Selecting);
            // 
            // tabPage1
            // 
            this.tabPage1.Controls.Add(this.cbxPresets);
            this.tabPage1.Controls.Add(this.label2);
            this.tabPage1.Controls.Add(this.label1);
            this.tabPage1.Controls.Add(this.button3);
            this.tabPage1.Controls.Add(this.button2);
            this.tabPage1.Controls.Add(this.button1);
            this.tabPage1.Controls.Add(this.btnWizard);
            this.tabPage1.Location = new System.Drawing.Point(4, 22);
            this.tabPage1.Name = "tabPage1";
            this.tabPage1.Padding = new System.Windows.Forms.Padding(10);
            this.tabPage1.Size = new System.Drawing.Size(506, 350);
            this.tabPage1.TabIndex = 0;
            this.tabPage1.Text = "Home";
            this.tabPage1.UseVisualStyleBackColor = true;
            this.tabPage1.Click += new System.EventHandler(this.tabPage1_Click);
            // 
            // cbxPresets
            // 
            this.cbxPresets.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.cbxPresets.FormattingEnabled = true;
            this.cbxPresets.Location = new System.Drawing.Point(158, 155);
            this.cbxPresets.Name = "cbxPresets";
            this.cbxPresets.Size = new System.Drawing.Size(194, 21);
            this.cbxPresets.TabIndex = 2;
            this.cbxPresets.SelectedIndexChanged += new System.EventHandler(this.cbxPresets_SelectedIndexChanged);
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(155, 136);
            this.label2.Margin = new System.Windows.Forms.Padding(3);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(87, 13);
            this.label2.TabIndex = 1;
            this.label2.Text = "Selected preset :";
            // 
            // label1
            // 
            this.label1.Location = new System.Drawing.Point(13, 13);
            this.label1.Margin = new System.Windows.Forms.Padding(3);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(480, 105);
            this.label1.TabIndex = 1;
            this.label1.Text = resources.GetString("label1.Text");
            // 
            // button3
            // 
            this.button3.Location = new System.Drawing.Point(158, 306);
            this.button3.Name = "button3";
            this.button3.Size = new System.Drawing.Size(194, 30);
            this.button3.TabIndex = 0;
            this.button3.Text = "Save preset as...";
            this.button3.UseVisualStyleBackColor = true;
            this.button3.Click += new System.EventHandler(this.button3_Click);
            // 
            // button2
            // 
            this.button2.Location = new System.Drawing.Point(158, 270);
            this.button2.Name = "button2";
            this.button2.Size = new System.Drawing.Size(194, 30);
            this.button2.TabIndex = 0;
            this.button2.Text = "Save preset";
            this.button2.UseVisualStyleBackColor = true;
            this.button2.Click += new System.EventHandler(this.button2_Click);
            // 
            // button1
            // 
            this.button1.Location = new System.Drawing.Point(158, 234);
            this.button1.Name = "button1";
            this.button1.Size = new System.Drawing.Size(194, 30);
            this.button1.TabIndex = 0;
            this.button1.Text = "Load preset...";
            this.button1.UseVisualStyleBackColor = true;
            this.button1.Click += new System.EventHandler(this.button1_Click);
            // 
            // btnWizard
            // 
            this.btnWizard.Location = new System.Drawing.Point(158, 198);
            this.btnWizard.Name = "btnWizard";
            this.btnWizard.Size = new System.Drawing.Size(194, 30);
            this.btnWizard.TabIndex = 0;
            this.btnWizard.Text = "Launch preset wizard";
            this.btnWizard.UseVisualStyleBackColor = true;
            this.btnWizard.Click += new System.EventHandler(this.btnWizard_Click);
            // 
            // tabPage2
            // 
            this.tabPage2.Controls.Add(this.lblPresetWarning);
            this.tabPage2.Controls.Add(this.btnCalibrate);
            this.tabPage2.Controls.Add(this.btnDeviceSettings);
            this.tabPage2.Controls.Add(this.btnAlgorithmSelection);
            this.tabPage2.Controls.Add(this.btnPresetName);
            this.tabPage2.Controls.Add(this.btnDeviceSelection);
            this.tabPage2.Location = new System.Drawing.Point(4, 22);
            this.tabPage2.Name = "tabPage2";
            this.tabPage2.Padding = new System.Windows.Forms.Padding(10);
            this.tabPage2.Size = new System.Drawing.Size(506, 350);
            this.tabPage2.TabIndex = 1;
            this.tabPage2.Text = "Preset settings";
            this.tabPage2.UseVisualStyleBackColor = true;
            // 
            // lblPresetWarning
            // 
            this.lblPresetWarning.Location = new System.Drawing.Point(13, 13);
            this.lblPresetWarning.Margin = new System.Windows.Forms.Padding(3);
            this.lblPresetWarning.Name = "lblPresetWarning";
            this.lblPresetWarning.Size = new System.Drawing.Size(480, 42);
            this.lblPresetWarning.TabIndex = 2;
            this.lblPresetWarning.Text = "No preset loaded !\r\nPlease use the preset wizard.";
            // 
            // btnCalibrate
            // 
            this.btnCalibrate.Location = new System.Drawing.Point(156, 234);
            this.btnCalibrate.Name = "btnCalibrate";
            this.btnCalibrate.Size = new System.Drawing.Size(194, 30);
            this.btnCalibrate.TabIndex = 1;
            this.btnCalibrate.Text = "Calibrate";
            this.btnCalibrate.UseVisualStyleBackColor = true;
            this.btnCalibrate.Click += new System.EventHandler(this.btnCalibrate_Click);
            // 
            // btnDeviceSettings
            // 
            this.btnDeviceSettings.Location = new System.Drawing.Point(156, 198);
            this.btnDeviceSettings.Name = "btnDeviceSettings";
            this.btnDeviceSettings.Size = new System.Drawing.Size(194, 30);
            this.btnDeviceSettings.TabIndex = 1;
            this.btnDeviceSettings.Text = "Device settings";
            this.btnDeviceSettings.UseVisualStyleBackColor = true;
            this.btnDeviceSettings.Click += new System.EventHandler(this.btnDeviceSettings_Click);
            // 
            // btnAlgorithmSelection
            // 
            this.btnAlgorithmSelection.Location = new System.Drawing.Point(156, 162);
            this.btnAlgorithmSelection.Name = "btnAlgorithmSelection";
            this.btnAlgorithmSelection.Size = new System.Drawing.Size(194, 30);
            this.btnAlgorithmSelection.TabIndex = 1;
            this.btnAlgorithmSelection.Text = "Select algorithm";
            this.btnAlgorithmSelection.UseVisualStyleBackColor = true;
            this.btnAlgorithmSelection.Click += new System.EventHandler(this.btnAlgorithmSelection_Click);
            // 
            // btnPresetName
            // 
            this.btnPresetName.Location = new System.Drawing.Point(156, 90);
            this.btnPresetName.Name = "btnPresetName";
            this.btnPresetName.Size = new System.Drawing.Size(194, 30);
            this.btnPresetName.TabIndex = 1;
            this.btnPresetName.Text = "Preset name";
            this.btnPresetName.UseVisualStyleBackColor = true;
            this.btnPresetName.Click += new System.EventHandler(this.btnPresetName_Click);
            // 
            // btnDeviceSelection
            // 
            this.btnDeviceSelection.Location = new System.Drawing.Point(156, 126);
            this.btnDeviceSelection.Name = "btnDeviceSelection";
            this.btnDeviceSelection.Size = new System.Drawing.Size(194, 30);
            this.btnDeviceSelection.TabIndex = 1;
            this.btnDeviceSelection.Text = "Select devices";
            this.btnDeviceSelection.UseVisualStyleBackColor = true;
            this.btnDeviceSelection.Click += new System.EventHandler(this.btnDeviceSelection_Click);
            // 
            // menuStrip1
            // 
            this.menuStrip1.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.fileToolStripMenuItem,
            this.settingsToolStripMenuItem,
            this.aboutToolStripMenuItem});
            this.menuStrip1.Location = new System.Drawing.Point(0, 0);
            this.menuStrip1.Name = "menuStrip1";
            this.menuStrip1.Size = new System.Drawing.Size(514, 24);
            this.menuStrip1.TabIndex = 1;
            this.menuStrip1.Text = "menuStrip1";
            // 
            // fileToolStripMenuItem
            // 
            this.fileToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.loadPresetToolStripMenuItem,
            this.savePresetToolStripMenuItem,
            this.savePresetToolStripMenuItem1,
            this.savePresetAsToolStripMenuItem,
            this.toolStripSeparator1,
            this.quitToolStripMenuItem});
            this.fileToolStripMenuItem.Name = "fileToolStripMenuItem";
            this.fileToolStripMenuItem.Size = new System.Drawing.Size(37, 20);
            this.fileToolStripMenuItem.Text = "File";
            // 
            // loadPresetToolStripMenuItem
            // 
            this.loadPresetToolStripMenuItem.Name = "loadPresetToolStripMenuItem";
            this.loadPresetToolStripMenuItem.Size = new System.Drawing.Size(185, 22);
            this.loadPresetToolStripMenuItem.Text = "Launch preset wizard";
            this.loadPresetToolStripMenuItem.Click += new System.EventHandler(this.loadPresetToolStripMenuItem_Click);
            // 
            // savePresetToolStripMenuItem
            // 
            this.savePresetToolStripMenuItem.Name = "savePresetToolStripMenuItem";
            this.savePresetToolStripMenuItem.Size = new System.Drawing.Size(185, 22);
            this.savePresetToolStripMenuItem.Text = "Load preset";
            // 
            // savePresetToolStripMenuItem1
            // 
            this.savePresetToolStripMenuItem1.Name = "savePresetToolStripMenuItem1";
            this.savePresetToolStripMenuItem1.Size = new System.Drawing.Size(185, 22);
            this.savePresetToolStripMenuItem1.Text = "Save preset";
            // 
            // savePresetAsToolStripMenuItem
            // 
            this.savePresetAsToolStripMenuItem.Name = "savePresetAsToolStripMenuItem";
            this.savePresetAsToolStripMenuItem.Size = new System.Drawing.Size(185, 22);
            this.savePresetAsToolStripMenuItem.Text = "Save preset as...";
            // 
            // toolStripSeparator1
            // 
            this.toolStripSeparator1.Name = "toolStripSeparator1";
            this.toolStripSeparator1.Size = new System.Drawing.Size(182, 6);
            // 
            // quitToolStripMenuItem
            // 
            this.quitToolStripMenuItem.Name = "quitToolStripMenuItem";
            this.quitToolStripMenuItem.Size = new System.Drawing.Size(185, 22);
            this.quitToolStripMenuItem.Text = "Quit";
            // 
            // settingsToolStripMenuItem
            // 
            this.settingsToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.performanceSettingsToolStripMenuItem,
            this.startCaptureToolStripMenuItem});
            this.settingsToolStripMenuItem.Name = "settingsToolStripMenuItem";
            this.settingsToolStripMenuItem.Size = new System.Drawing.Size(61, 20);
            this.settingsToolStripMenuItem.Text = "Settings";
            // 
            // performanceSettingsToolStripMenuItem
            // 
            this.performanceSettingsToolStripMenuItem.Name = "performanceSettingsToolStripMenuItem";
            this.performanceSettingsToolStripMenuItem.Size = new System.Drawing.Size(200, 22);
            this.performanceSettingsToolStripMenuItem.Text = "Performance settings";
            // 
            // startCaptureToolStripMenuItem
            // 
            this.startCaptureToolStripMenuItem.Name = "startCaptureToolStripMenuItem";
            this.startCaptureToolStripMenuItem.Size = new System.Drawing.Size(200, 22);
            this.startCaptureToolStripMenuItem.Text = "Start whiteboard engine";
            this.startCaptureToolStripMenuItem.Click += new System.EventHandler(this.startCaptureToolStripMenuItem_Click);
            // 
            // aboutToolStripMenuItem
            // 
            this.aboutToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.helpToolStripMenuItem,
            this.aboutWolfEyesToolStripMenuItem});
            this.aboutToolStripMenuItem.Name = "aboutToolStripMenuItem";
            this.aboutToolStripMenuItem.Size = new System.Drawing.Size(24, 20);
            this.aboutToolStripMenuItem.Text = "?";
            // 
            // helpToolStripMenuItem
            // 
            this.helpToolStripMenuItem.Name = "helpToolStripMenuItem";
            this.helpToolStripMenuItem.Size = new System.Drawing.Size(161, 22);
            this.helpToolStripMenuItem.Text = "Help";
            // 
            // aboutWolfEyesToolStripMenuItem
            // 
            this.aboutWolfEyesToolStripMenuItem.Name = "aboutWolfEyesToolStripMenuItem";
            this.aboutWolfEyesToolStripMenuItem.Size = new System.Drawing.Size(161, 22);
            this.aboutWolfEyesToolStripMenuItem.Text = "About Wolf Eyes";
            // 
            // panel1
            // 
            this.panel1.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D;
            this.panel1.Controls.Add(this.lblEngine);
            this.panel1.Controls.Add(this.lblLoadedPreset);
            this.panel1.Controls.Add(this.label4);
            this.panel1.Controls.Add(this.label3);
            this.panel1.Dock = System.Windows.Forms.DockStyle.Bottom;
            this.panel1.Location = new System.Drawing.Point(0, 400);
            this.panel1.Name = "panel1";
            this.panel1.Size = new System.Drawing.Size(514, 26);
            this.panel1.TabIndex = 3;
            // 
            // lblEngine
            // 
            this.lblEngine.AutoSize = true;
            this.lblEngine.Location = new System.Drawing.Point(448, 5);
            this.lblEngine.Name = "lblEngine";
            this.lblEngine.Size = new System.Drawing.Size(45, 13);
            this.lblEngine.TabIndex = 3;
            this.lblEngine.Text = "stopped";
            // 
            // lblLoadedPreset
            // 
            this.lblLoadedPreset.AutoSize = true;
            this.lblLoadedPreset.Location = new System.Drawing.Point(97, 5);
            this.lblLoadedPreset.Name = "lblLoadedPreset";
            this.lblLoadedPreset.Size = new System.Drawing.Size(31, 13);
            this.lblLoadedPreset.TabIndex = 3;
            this.lblLoadedPreset.Text = "none";
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(396, 5);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(46, 13);
            this.label4.TabIndex = 3;
            this.label4.Text = "Engine :";
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(10, 5);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(81, 13);
            this.label3.TabIndex = 3;
            this.label3.Text = "Loaded preset :";
            // 
            // saveFileDialog1
            // 
            this.saveFileDialog1.FileName = "noname";
            this.saveFileDialog1.Filter = "Wolf Eyes Preset | *.wpr";
            this.saveFileDialog1.FileOk += new System.ComponentModel.CancelEventHandler(this.saveFileDialog1_FileOk);
            // 
            // openFileDialog1
            // 
            this.openFileDialog1.Filter = "Wolf Eyes Preset | *.wpr";
            this.openFileDialog1.FileOk += new System.ComponentModel.CancelEventHandler(this.openFileDialog1_FileOk);
            // 
            // FrmMain
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(514, 426);
            this.Controls.Add(this.tabControl1);
            this.Controls.Add(this.panel1);
            this.Controls.Add(this.menuStrip1);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedDialog;
            this.MainMenuStrip = this.menuStrip1;
            this.MaximizeBox = false;
            this.Name = "FrmMain";
            this.ShowIcon = false;
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "Wolf Eyes - 0.15.1214a";
            this.FormClosing += new System.Windows.Forms.FormClosingEventHandler(this.FrmMain_FormClosing);
            this.Load += new System.EventHandler(this.FrmMain_Load);
            this.tabControl1.ResumeLayout(false);
            this.tabPage1.ResumeLayout(false);
            this.tabPage1.PerformLayout();
            this.tabPage2.ResumeLayout(false);
            this.menuStrip1.ResumeLayout(false);
            this.menuStrip1.PerformLayout();
            this.panel1.ResumeLayout(false);
            this.panel1.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.TabControl tabControl1;
        private System.Windows.Forms.TabPage tabPage1;
        private System.Windows.Forms.MenuStrip menuStrip1;
        private System.Windows.Forms.ToolStripMenuItem fileToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem loadPresetToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem savePresetToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem savePresetAsToolStripMenuItem;
        private System.Windows.Forms.ToolStripSeparator toolStripSeparator1;
        private System.Windows.Forms.ToolStripMenuItem quitToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem settingsToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem performanceSettingsToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem aboutToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem helpToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem aboutWolfEyesToolStripMenuItem;
        private System.Windows.Forms.Button btnWizard;
        private System.Windows.Forms.ToolStripMenuItem startCaptureToolStripMenuItem;
        private System.Windows.Forms.ComboBox cbxPresets;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Button button3;
        private System.Windows.Forms.Button button2;
        private System.Windows.Forms.Button button1;
        private System.Windows.Forms.TabPage tabPage2;
        private System.Windows.Forms.Button btnCalibrate;
        private System.Windows.Forms.Button btnDeviceSettings;
        private System.Windows.Forms.Button btnAlgorithmSelection;
        private System.Windows.Forms.Button btnDeviceSelection;
        private System.Windows.Forms.Label lblPresetWarning;
        private System.Windows.Forms.Button btnPresetName;
        private System.Windows.Forms.Panel panel1;
        private System.Windows.Forms.Label lblLoadedPreset;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.Label lblEngine;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.SaveFileDialog saveFileDialog1;
        private System.Windows.Forms.OpenFileDialog openFileDialog1;
        private System.Windows.Forms.ToolStripMenuItem savePresetToolStripMenuItem1;
    }
}

