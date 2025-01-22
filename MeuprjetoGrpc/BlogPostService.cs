using Grpc.Core;
using MeuProjetoGrpc.Protos;

namespace MeuProjetoGrpc.Services {
    public class BlogPostsService : BlogPosts.BlogPostsBase {
        public override Task<CreateBlogPostResponse> CreateBlogPost(CreateBlogPostRequest request, ServerCallContext context) {
            // Lógica para criar um blog post
            return Task.FromResult(new CreateBlogPostResponse { Id = Guid.NewGuid().ToString() });
        }
    }
}