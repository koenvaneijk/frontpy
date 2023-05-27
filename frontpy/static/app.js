async function main() {
    let pyodide = await loadPyodide();
    await pyodide.runPythonAsync(`
    from pyodide.http import pyfetch

    response = await pyfetch("frontend")
    
    with open("web.py", "wb") as f:
        f.write(await response.bytes())

    response0 = await pyfetch("ui")
    
    with open("ui.py", "wb") as f:
        f.write(await response0.bytes())                
`)
    ui = pyodide.pyimport("ui");
    pkg = pyodide.pyimport("web");
    pkg.main();
};

main(); // Run the main function