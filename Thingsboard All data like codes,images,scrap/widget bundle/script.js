self.onInit = function() {
    self.ctx.$scope = self.ctx.$scope || {};
    self.ctx.$scope.data = self.ctx.$scope.data || [];
    self.ctx.$scope.auditLogs = self.ctx.$scope.auditLogs || [];
  };
  
  self.onDataUpdated = function() {
    if (self.ctx.$scope) {
      self.ctx.detectChanges();
    }
  };
  
  function WebSocketAPIExample() {
    var token = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0ZWFtQGNvbnRyb2x5dGljcy5haSIsInVzZXJJZCI6IjY2MGU0YmIwLTQyOTQtMTFlZS1hZjJjLTFkZDc1YzkwNjQ1YiIsInNjb3BlcyI6WyJURU5BTlRfQURNSU4iXSwic2Vzc2lvbklkIjoiNDBhOTUwZTAtYjBiYy00ZGZhLTllOGMtZTJmN2M1NzU0MmY3IiwiaXNzIjoidGhpbmdzYm9hcmQuaW8iLCJpYXQiOjE3MDQ5NzU0MjQsImV4cCI6MTcwNDk4NDQyNCwiZW5hYmxlZCI6dHJ1ZSwiaXNQdWJsaWMiOmZhbHNlLCJ0ZW5hbnRJZCI6IjVhNjU4NjIwLTQyOTQtMTFlZS1hZjJjLTFkZDc1YzkwNjQ1YiIsImN1c3RvbWVySWQiOiIxMzgxNDAwMC0xZGQyLTExYjItODA4MC04MDgwODA4MDgwODAifQ.FYgaz0cHr1PhAZP30atje00c8lKIvC3MMNu6zB14SH-AxhJb8Cr2qE09sbrFXZe3ntZa061ax28vimAe9WDtPw";
    var auditLogsUrl = "http://app.controlytics.ai/api/auth/login";
  
    // Fetch audit logs from the provided URL
    fetch(auditLogsUrl, {
      method: 'GET',
      headers: {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
      }
    })
    .then(response => response.json())
    .then(auditLogs => {
      // Ensure that self.ctx.$scope is initialized
      self.ctx.$scope = self.ctx.$scope || {};
  
      // Append the fetched audit logs to the existing ones
      self.ctx.$scope.auditLogs = self.ctx.$scope.auditLogs.concat(auditLogs);
  
      // Process audit logs and update widget data
      processAuditLogs();
  
      // Update the widget with the new data
      self.ctx.$scope && self.ctx.detectChanges();
    })
    .catch(error => {
      console.error('Error fetching audit logs:', error);
    });
  
    function processAuditLogs() {
      self.ctx.$scope = self.ctx.$scope || {};
      self.ctx.$scope.auditLogs = self.ctx.$scope.auditLogs || [];
  
      self.ctx.$scope.auditLogs.forEach(function(log) {
        var logEntry = {
          user: log.userName,
          status: log.actionStatus,
          type: log.type,
          entityName: log.entityName,
          entityType: log.entityType,
          timestamp: log.timestamp
        };
  
        // Ensure that self.ctx.$scope.data is initialized
        self.ctx.$scope.data = self.ctx.$scope.data || [];
  
        // Add the log entry to the widget data
        self.ctx.$scope.data.push(logEntry);
      });
    }
  }
  