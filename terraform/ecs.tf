resource "aws_ecs_cluster" "main" {
  name = "factura-cluster"
}

resource "aws_ecs_task_definition" "factura_task" {
  family                   = "factura-task"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = "256"
  memory                   = "512"

  container_definitions = jsonencode([
    {
      name      = "procesar"
      image     = "TU_ECR_REPO/procesar:latest"
      essential = true
      portMappings = [
        {
          containerPort = 8000
          hostPort      = 8000
        }
      ]
    },
    {
      name      = "consultar"
      image     = "TU_ECR_REPO/consultar:latest"
      essential = true
      portMappings = [
        {
          containerPort = 8001
          hostPort      = 8001
        }
      ]
    }
  ])
}

resource "aws_ecs_service" "factura_service" {
  name            = "factura-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.factura_task.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets         = ["SUBNET_ID"]
    assign_public_ip = true
    security_groups = ["SECURITY_GROUP_ID"]
  }
}
