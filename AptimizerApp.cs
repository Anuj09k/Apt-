using System;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Net.Sockets;
using System.ServiceProcess;
using System.Threading;
using System.Windows.Forms;

namespace Aptimizer
{
    public class AptimizerTrayApp : ApplicationContext
    {
        private NotifyIcon trayIcon;
        private ContextMenuStrip trayMenu;
        private string baseDir;
        private Process backendProcess;
        private Process frontendProcess;

        public AptimizerTrayApp()
        {
            baseDir = ResolveBaseDir();

            // 1. Setup System Tray first so user gets visual feedback immediately
            SetupTray();

            trayIcon.ShowBalloonTip(4000, "Aptimizer Civil AI", "Starting services... Please wait while the application initializes.", ToolTipIcon.Info);

            // 2. Ensure Services are Running
            EnsureMongoRunning();
            EnsureBackendRunning();
            EnsureFrontendRunning();

            // 3. Wait for Frontend (React/craco webpack compilation takes 15-30 seconds on cold start)
            bool ready = WaitForPort(3000, 45);

            // 4. Launch App Window
            if (ready)
            {
                trayIcon.ShowBalloonTip(3000, "Aptimizer Civil AI", "Application is ready! Opening window...", ToolTipIcon.Info);
                LaunchAppWindow();
            }
            else
            {
                MessageBox.Show(
                    "Frontend service (http://localhost:3000) did not respond within 45 seconds.\n\n" +
                    "Please ensure Node.js is installed or start manually using dev.bat in:\n" + baseDir,
                    "Aptimizer Startup", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            }
        }

        private static string ResolveBaseDir()
        {
            // 1. Current app domain base directory (e.g. when run from project folder)
            string current = AppDomain.CurrentDomain.BaseDirectory;
            if (Directory.Exists(Path.Combine(current, "backend")) && Directory.Exists(Path.Combine(current, "frontend")))
            {
                return current;
            }

            // 2. Assembly location directory
            string asmLoc = Path.GetDirectoryName(System.Reflection.Assembly.GetExecutingAssembly().Location);
            if (!string.IsNullOrEmpty(asmLoc) && Directory.Exists(Path.Combine(asmLoc, "backend")) && Directory.Exists(Path.Combine(asmLoc, "frontend")))
            {
                return asmLoc;
            }

            // 3. Check parent directories
            try
            {
                DirectoryInfo parent = Directory.GetParent(current);
                while (parent != null)
                {
                    if (Directory.Exists(Path.Combine(parent.FullName, "backend")) && Directory.Exists(Path.Combine(parent.FullName, "frontend")))
                    {
                        return parent.FullName;
                    }
                    parent = parent.Parent;
                }
            }
            catch { }

            // 4. Known project directory on this system
            string knownDir = @"c:\Users\Anuj1\Downloads\Jules Apt";
            if (Directory.Exists(Path.Combine(knownDir, "backend")) && Directory.Exists(Path.Combine(knownDir, "frontend")))
            {
                return knownDir;
            }

            // 5. Stored config in %APPDATA%\Aptimizer\project_path.txt
            try
            {
                string cfg = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData), "Aptimizer", "project_path.txt");
                if (File.Exists(cfg))
                {
                    string saved = File.ReadAllText(cfg).Trim();
                    if (Directory.Exists(Path.Combine(saved, "backend")) && Directory.Exists(Path.Combine(saved, "frontend")))
                    {
                        return saved;
                    }
                }
            }
            catch { }

            // 6. User selection fallback
            using (FolderBrowserDialog fbd = new FolderBrowserDialog())
            {
                fbd.Description = "Select Aptimizer project folder (containing 'backend' and 'frontend'):";
                if (fbd.ShowDialog() == DialogResult.OK)
                {
                    if (Directory.Exists(Path.Combine(fbd.SelectedPath, "backend")) && Directory.Exists(Path.Combine(fbd.SelectedPath, "frontend")))
                    {
                        try
                        {
                            string cfg = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData), "Aptimizer", "project_path.txt");
                            string dir = Path.GetDirectoryName(cfg);
                            if (!Directory.Exists(dir)) Directory.CreateDirectory(dir);
                            File.WriteAllText(cfg, fbd.SelectedPath);
                        }
                        catch { }
                        return fbd.SelectedPath;
                    }
                }
            }

            return current;
        }

        private void SetupTray()
        {
            trayMenu = new ContextMenuStrip();

            ToolStripMenuItem itemOpen = new ToolStripMenuItem("Open Aptimizer Window", null, (s, e) => LaunchAppWindow());
            itemOpen.Font = new Font(itemOpen.Font, FontStyle.Bold);

            ToolStripMenuItem itemPdf = new ToolStripMenuItem("Open Built Features Guide (PDF)", null, (s, e) => OpenPdf());
            ToolStripMenuItem itemFolder = new ToolStripMenuItem("Open Project Folder", null, (s, e) => OpenFolder());
            ToolStripSeparator sep = new ToolStripSeparator();
            ToolStripMenuItem itemExit = new ToolStripMenuItem("Exit & Stop Services", null, (s, e) => ExitApp());

            trayMenu.Items.Add(itemOpen);
            trayMenu.Items.Add(itemPdf);
            trayMenu.Items.Add(itemFolder);
            trayMenu.Items.Add(sep);
            trayMenu.Items.Add(itemExit);

            trayIcon = new NotifyIcon();
            trayIcon.Text = "Aptimizer Civil AI Platform";
            trayIcon.ContextMenuStrip = trayMenu;
            trayIcon.Visible = true;

            string iconPath = Path.Combine(baseDir, @"frontend\public\favicon.ico");
            if (File.Exists(iconPath))
            {
                try { trayIcon.Icon = new Icon(iconPath); }
                catch { trayIcon.Icon = SystemIcons.Application; }
            }
            else
            {
                trayIcon.Icon = SystemIcons.Application;
            }

            trayIcon.DoubleClick += (s, e) => LaunchAppWindow();
        }

        private void OpenPdf()
        {
            string pdfPath = Path.Combine(baseDir, "Aptimizer_Built_Features_Plain_English_Guide.pdf");
            if (File.Exists(pdfPath))
            {
                Process.Start(pdfPath);
            }
            else
            {
                MessageBox.Show("PDF Guide file not found in project folder:\n" + pdfPath, "Aptimizer", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            }
        }

        private void OpenFolder()
        {
            Process.Start("explorer.exe", baseDir);
        }

        private void LaunchAppWindow()
        {
            string url = "http://localhost:3000";

            string[] candidateBrowsers = new string[]
            {
                @"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                @"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
                @"C:\Program Files\Google\Chrome\Application\chrome.exe",
                @"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
            };

            foreach (string exe in candidateBrowsers)
            {
                if (File.Exists(exe))
                {
                    try
                    {
                        Process.Start(exe, string.Format("--app={0} --window-size=1440,920", url));
                        return;
                    }
                    catch { }
                }
            }

            try
            {
                Process.Start(url);
            }
            catch (Exception ex)
            {
                MessageBox.Show("Could not launch browser: " + ex.Message, "Aptimizer", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private bool IsPortInUse(int port)
        {
            return Program.IsPortInUseStatic(port);
        }

        private bool WaitForPort(int port, int maxSeconds)
        {
            for (int i = 0; i < maxSeconds * 2; i++)
            {
                if (IsPortInUse(port)) return true;
                Thread.Sleep(500);
            }
            return false;
        }

        private void EnsureMongoRunning()
        {
            try
            {
                if (IsPortInUse(27017)) return;
                ServiceController sc = new ServiceController("MongoDB");
                if (sc.Status != ServiceControllerStatus.Running && sc.Status != ServiceControllerStatus.StartPending)
                {
                    sc.Start();
                    sc.WaitForStatus(ServiceControllerStatus.Running, TimeSpan.FromSeconds(5));
                }
            }
            catch { }
        }

        private void EnsureBackendRunning()
        {
            if (IsPortInUse(8000)) return;

            string backendDir = Path.Combine(baseDir, "backend");
            if (!Directory.Exists(backendDir)) return;

            ProcessStartInfo psi = new ProcessStartInfo();
            psi.FileName = "cmd.exe";
            psi.Arguments = "/c python -m uvicorn server:app --host 127.0.0.1 --port 8000";
            psi.WorkingDirectory = backendDir;
            psi.WindowStyle = ProcessWindowStyle.Hidden;
            psi.CreateNoWindow = true;
            psi.UseShellExecute = false;

            try
            {
                backendProcess = Process.Start(psi);
                WaitForPort(8000, 15);
            }
            catch { }
        }

        private void EnsureFrontendRunning()
        {
            if (IsPortInUse(3000)) return;

            string frontendDir = Path.Combine(baseDir, "frontend");
            if (!Directory.Exists(frontendDir)) return;

            ProcessStartInfo psi = new ProcessStartInfo();
            psi.FileName = "cmd.exe";
            psi.Arguments = "/c set BROWSER=none&& npm start";
            psi.WorkingDirectory = frontendDir;
            psi.WindowStyle = ProcessWindowStyle.Hidden;
            psi.CreateNoWindow = true;
            psi.UseShellExecute = false;

            try
            {
                frontendProcess = Process.Start(psi);
            }
            catch { }
        }

        private void KillPort(int port)
        {
            try
            {
                ProcessStartInfo psi = new ProcessStartInfo();
                psi.FileName = "cmd.exe";
                psi.Arguments = string.Format("/c for /f \"tokens=5\" %a in ('netstat -ano ^| findstr \":{0} \" ^| findstr \"LISTENING\"') do taskkill /PID %a /F", port);
                psi.WindowStyle = ProcessWindowStyle.Hidden;
                psi.CreateNoWindow = true;
                psi.UseShellExecute = false;
                Process.Start(psi);
            }
            catch { }
        }

        private void ExitApp()
        {
            trayIcon.Visible = false;

            // Stop background processes if created
            if (backendProcess != null && !backendProcess.HasExited)
            {
                try { backendProcess.Kill(); } catch { }
            }
            if (frontendProcess != null && !frontendProcess.HasExited)
            {
                try { frontendProcess.Kill(); } catch { }
            }

            // Stop listening ports
            KillPort(8000);
            KillPort(3000);

            Application.Exit();
        }
    }

    static class Program
    {
        private static Mutex mutex = null;

        [STAThread]
        static void Main()
        {
            const string appName = "AptimizerCivilAI_SingleInstance";
            bool createdNew;

            mutex = new Mutex(true, appName, out createdNew);

            if (!createdNew)
            {
                // Already running - check if port 3000 is active
                if (IsPortInUseStatic(3000))
                {
                    LaunchExisting();
                    return;
                }
                else
                {
                    DialogResult res = MessageBox.Show(
                        "An Aptimizer background process is already registered, but the application services are not responding on port 3000.\n\nWould you like to restart Aptimizer services?",
                        "Aptimizer Already Running", MessageBoxButtons.YesNo, MessageBoxIcon.Question);
                    if (res == DialogResult.Yes)
                    {
                        try
                        {
                            int currentPid = Process.GetCurrentProcess().Id;
                            foreach (Process p in Process.GetProcessesByName("Aptimizer"))
                            {
                                if (p.Id != currentPid)
                                {
                                    try { p.Kill(); } catch { }
                                }
                            }
                        }
                        catch { }
                        Thread.Sleep(800);
                    }
                    else
                    {
                        return;
                    }
                }
            }

            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new AptimizerTrayApp());
        }

        public static bool IsPortInUseStatic(int port)
        {
            try
            {
                using (TcpClient client = new TcpClient())
                {
                    IAsyncResult result = client.BeginConnect("127.0.0.1", port, null, null);
                    bool success = result.AsyncWaitHandle.WaitOne(400);
                    if (!success) return false;
                    client.EndConnect(result);
                    return true;
                }
            }
            catch
            {
                return false;
            }
        }

        static void LaunchExisting()
        {
            string url = "http://localhost:3000";
            string[] candidateBrowsers = new string[]
            {
                @"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                @"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
                @"C:\Program Files\Google\Chrome\Application\chrome.exe"
            };

            foreach (string exe in candidateBrowsers)
            {
                if (File.Exists(exe))
                {
                    try { Process.Start(exe, string.Format("--app={0} --window-size=1440,920", url)); return; }
                    catch { }
                }
            }

            Process.Start(url);
        }
    }
}
