"""Manager Agent core orchestration logic"""

import asyncio
from typing import Dict, Any, Optional, List
from datetime import datetime

from .messages import (
  ExtractionRequest, ExtractionResponse,
  GenerationRequest, GenerationResponse,
  RLUpdateRequest, RLRecommendation,
  ManagerCommand, ContentType, LearningMode
)
from .memory import load_state, save_state, reset_state, RLState
from .logger import logger


class ManagerAgent:
  """Orchestrates all agents and manages workflow"""
    
  def __init__(self, username: Optional[str] = None):
    self.logger = logger.get_logger()
    self.session_context: Dict[str, Any] = {}
    self.username = username
    self.state: RLState = load_state(username)

  def handle_command(self, command: ManagerCommand) -> Dict[str, Any]:
    """Handle a manager command synchronously"""
    try:
      # Add session_id to params if provided
      params = command.params.copy() if command.params else {}
      if command.session_id:
        params["session_id"] = command.session_id
      
      if command.action == "extract":
        return self._handle_extract(params)
      elif command.action == "generate":
        return self._handle_generate(params)
      elif command.action == "update_rl":
        return self._handle_update_rl(params)
      elif command.action == "recommend":
        return self._handle_recommend(params)
      elif command.action == "survey":
        return self._handle_survey(params)
      elif command.action == "reset_preferences":
        return self._handle_reset_preferences()
      else:
        return {"success": False, "error": f"Unknown action: {command.action}"}
    except Exception as e:
      self.logger.exception(f"Error handling command {command.action}")
      return {"success": False, "error": str(e)}

    async def handle_command_async(self, command: ManagerCommand) -> Dict[str, Any]:
      """Handle a manager command asynchronously (for parallel agent calls)"""
      # Future enhancement: use asyncio.gather for parallel operations
      return self.handle_command(command)
    
    def _handle_extract(self, params: Dict[str, Any]) -> Dict[str, Any]:
      """Route extraction request to NLP Agent"""
      from ..agents.nlp_agent import NLPAgent
      
      nlp_agent = NLPAgent()
      # Remove session_id from params as ExtractionRequest doesn't accept it
      extract_params = {k: v for k, v in params.items() if k in ['file_path', 'file_content', 'file_type']}
      request = ExtractionRequest(**extract_params)
      response = nlp_agent.extract(request)
      
      # Store in session context
      session_id = params.get("session_id")
      self.logger.info(f"Extract handler - session_id: {session_id}, chunks count: {len(response.chunks) if response.chunks else 0}")
      
      if session_id:
          self.session_context[session_id] = {
              "chunks": response.chunks,
              "summary": response.summary
          }
          self.logger.info(f"Stored {len(response.chunks)} chunks in session {session_id} (total {sum(len(c) for c in response.chunks)} chars)")
          self.logger.info(f"Session context keys: {list(self.session_context.keys())}")
      else:
          self.logger.warning("No session_id provided in extract params, chunks will not be stored in session context")
      
      return {
          "success": response.success,
          "chunks": response.chunks,
          "summary": response.summary,
          "error": response.error
      }

