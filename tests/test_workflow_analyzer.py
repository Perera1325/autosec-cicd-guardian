from src.workflow_analyzer import scan_all_workflows

def test_scan_all_workflows():
    report = scan_all_workflows()
    assert "total_files_scanned" in report
    assert "files" in report
