/*
 * Copyright (c) 2022 Airbyte, Inc., all rights reserved.
 */

package io.airbyte.server.handlers;

import io.airbyte.api.model.generated.InternalOperationResult;
import io.airbyte.api.model.generated.SaveStatsRequestBody;
import io.airbyte.api.model.generated.SetWorkflowInAttemptRequestBody;
import io.airbyte.config.JobOutput;
import io.airbyte.persistence.job.JobPersistence;
import java.io.IOException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class AttemptHandler {

  private static final Logger LOGGER = LoggerFactory.getLogger(AttemptHandler.class);

  private final JobPersistence jobPersistence;

  public AttemptHandler(JobPersistence jobPersistence) {
    this.jobPersistence = jobPersistence;
  }

  public InternalOperationResult setWorkflowInAttempt(
                                                      SetWorkflowInAttemptRequestBody requestBody) {
    try {
      jobPersistence.setAttemptTemporalWorkflowInfo(requestBody.getJobId(),
          requestBody.getAttemptNumber(), requestBody.getWorkflowId().toString(), requestBody.getProcessingTaskQueue());
    } catch (IOException ioe) {
      LOGGER.error("IOException when setting temporal workflow in attempt;", ioe);
      return new InternalOperationResult().succeeded(false);
    }
    return new InternalOperationResult().succeeded(true);
  }

  public InternalOperationResult saveStats(SaveStatsRequestBody requestBody) {
    try {
      // This is for the entire sync for now.
      final var stats = requestBody.getStats();
      jobPersistence.writeSyncStats(requestBody.getJobId(), requestBody.getAttemptNumber(),
          stats.getEstimatedRecords(), stats.getEstimatedBytes(), stats.getRecordsEmitted(), stats.getBytesEmitted());
    } catch (IOException ioe) {
      LOGGER.error("IOException when setting temporal workflow in attempt;", ioe);
      return new InternalOperationResult().succeeded(false);
    }

    return new InternalOperationResult().succeeded(true);
  }



}
