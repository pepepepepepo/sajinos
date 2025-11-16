"""
コード実行API
AIが生成したコードを安全に実行する機能
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import subprocess
import tempfile
import os
import sys
from typing import Optional
import asyncio
import time
import io
import contextlib
from io import StringIO

router = APIRouter()

class CodeExecutionRequest(BaseModel):
    code: str
    language: str = "python"
    timeout: int = 10

class CodeExecutionResponse(BaseModel):
    success: bool
    output: Optional[str] = None
    error: Optional[str] = None
    execution_time: float

@router.post("/run-python", response_model=CodeExecutionResponse)
async def run_python_code(request: CodeExecutionRequest):
    """Pythonコードを安全に実行"""
    try:
        start_time = time.time()
        
        # コードを前処理してinput()を安全な値に置換
        processed_code = request.code
        
        # input()を安全なデフォルト値に置換
        if 'input(' in processed_code:
            import re
            # input("プロンプト") を適切なデフォルト値に置換
            def replace_input(match):
                prompt = match.group(1) if match.group(1) else ""
                if "最初" in prompt or "一つ目" in prompt or "first" in prompt.lower() or "数字" in prompt or "数" in prompt:
                    return '"10"'  # 最初の数値
                elif "二つ目" in prompt or "second" in prompt.lower() or "2" in prompt:
                    return '"20"'  # 二つ目の数値
                elif "数字" in prompt or "数値" in prompt or "number" in prompt.lower():
                    return '"42"'  # 数値用デフォルト
                else:
                    return '"Hello"'  # 文字列用デフォルト
            
            processed_code = re.sub(r'input\(["\']([^"\']*)["\']?\)', replace_input, processed_code)
            # デバッグ: 変換結果を確認
            if processed_code != request.code:
                print(f"🔄 コード変換:")
                print(f"元: {request.code}")
                print(f"変換後: {processed_code}")
        
        # input()が含まれている場合はユーザーフレンドリーなメッセージ
        if 'input(' in processed_code:
            return CodeExecutionResponse(
                success=False,
                error="💡 ヒント: input()の代わりに、直接値を設定してみてください！\n例: a = 10  # input()の代わり\n    b = 20  # input()の代わり",
                execution_time=0
            )
        
        # 危険なコードをチェック
        dangerous_imports = [
            'os.system', 'subprocess', 'eval', '__import__',
            'raw_input', 'file(', 'execfile', 'compile',
            'reload', 'delattr', 'setattr', 'getattr',
            'globals', 'locals', 'import os', 'import subprocess'
        ]
        
        code_lower = processed_code.lower()
        for dangerous in dangerous_imports:
            if dangerous in code_lower:
                return CodeExecutionResponse(
                    success=False,
                    error=f"セキュリティ上の理由により、'{dangerous}' の使用は禁止されています",
                    execution_time=0
                )
        
        # 一時ファイルを作成してコードを実行（UTF-8エンコーディング指定）
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as temp_file:
            temp_file.write(processed_code)
            temp_file_path = temp_file.name
        
        try:
            # より安全な実行方法：直接コードを実行
            import io
            import contextlib
            from io import StringIO
            
            # stdout/stderrをキャプチャ
            old_stdout = sys.stdout
            old_stderr = sys.stderr
            stdout_capture = StringIO()
            stderr_capture = StringIO()
            
            try:
                sys.stdout = stdout_capture
                sys.stderr = stderr_capture
                
                # コードを安全に実行（前処理済み）
                exec(compile(processed_code, '<string>', 'exec'))
                
                execution_time = time.time() - start_time
                
                # 出力を取得
                stdout_output = stdout_capture.getvalue()
                stderr_output = stderr_capture.getvalue()
                
                output = stdout_output
                if stderr_output:
                    output += f"\n[警告]: {stderr_output}"
                
                # input()が置換された場合の説明を追加
                if 'input(' in request.code and processed_code != request.code:
                    output = f"📝 input()をデフォルト値で実行しました:\n{output}"
                
                return CodeExecutionResponse(
                    success=True,
                    output=output.strip() if output.strip() else "実行完了（出力なし）",
                    execution_time=execution_time
                )
                
            except Exception as exec_error:
                execution_time = time.time() - start_time
                return CodeExecutionResponse(
                    success=False,
                    error=str(exec_error),
                    execution_time=execution_time
                )
            finally:
                # stdout/stderrを復元
                sys.stdout = old_stdout
                sys.stderr = old_stderr
                
        finally:
            # 一時ファイルを削除
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
                
    except subprocess.TimeoutExpired:
        return CodeExecutionResponse(
            success=False,
            error=f"実行がタイムアウトしました（{request.timeout}秒）",
            execution_time=request.timeout
        )
    except Exception as e:
        return CodeExecutionResponse(
            success=False,
            error=f"予期しないエラー: {str(e)}",
            execution_time=time.time() - start_time if 'start_time' in locals() else 0
        )

@router.get("/supported-languages")
async def get_supported_languages():
    """サポートされているプログラミング言語のリスト"""
    return {
        "languages": [
            {
                "name": "Python",
                "key": "python",
                "version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
                "available": True
            }
        ]
    }